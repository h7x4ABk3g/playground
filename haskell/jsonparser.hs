-- Written as an exercise from this amazing lecture:
-- https://www.youtube.com/watch?v=N9RUqGYuGfw

module Main where

import Control.Applicative
import Data.Char (isSpace, isDigit)
import Data.Functor((<&>))
import System.Directory(doesFileExist)

data JsonValue
  = JsonNull
  | JsonBool Bool
  | JsonNumber Integer
  | JsonString String
  | JsonArray [JsonValue]
  | JsonObject [(String, JsonValue)]
  deriving (Show, Eq)

-- Could have been:            row  col  error    key    val
-- parser :: String -> Either (Int, Int, String) (String, a)

-- Kind of a class containing one method, only the object becomes the first
-- parameter of the method. This is actually a trick, since records are usually
-- meant for datatypes.
newtype Parser a = Parser
  --                                rest of input, parsed value
  { runParser :: String -> Maybe (String, a)
  }

--       char -> parser that parses the specific char
charP :: Char -> Parser Char
charP x = Parser f
  where
      f (y:ys)
        | y == x = Just (ys, x)
        -- fail if the characters don't match
        | otherwise = Nothing
      -- in case there is no input left, it should also fail
      f [] = Nothing

-- Here, we would like a function that combines char parsers
-- into a string parser. Hence the name 'Parser Combinator'
-- [Parser Char] -> Parser [Char]

-- We have a really good function for this in haskell:
-- sequenceA :: Applicative f => t (f a) -> f (t a)
-- We need parser to be applicative in order for this to work.
-- In order to do this, it also needs to be a functor.

instance Functor Parser where
  -- fmap :: Functor f => (a -> b) -> f a -> f b
  fmap f (Parser p) = Parser f'
    where
      f' input = do
        (input', x) <- p input
        Just (input', f x)

instance Applicative Parser where
  -- Parser that ignores any input, but only returns a specific value
  -- on runParser
  -- pure :: Applicative f => a -> f a
  pure x = Parser $ \input -> Just (input, x)

  -- for chaining of operations (or chaining of parsers):
  -- (<*>) :: Applicative f => f (a -> b) -> f a -> f b
  (Parser p1) <*> (Parser p2) = Parser f
    where
      f input = do
        (input', f') <- p1 input
        (input'', a) <- p2 input'
        Just (input'', f' a)


--         String -> parser that parses the specific string
stringP :: String -> Parser String
stringP = sequenceA . map charP
-- Could have used 'traverse'

jsonNull :: Parser JsonValue
-- This fmap operation will only succeed if the parser succeeded.
-- Else, it all becomes Nothing
jsonNull = const JsonNull <$> stringP "null"

-- Here, we will need two parsers that parses either 'true' or 'false'
-- and combine them somehow
-- There is a typeclass for that in Control.Applicative called "Alternative"
-- It works kind of like implementing the JS || or ?? operator

instance Alternative Parser where
  -- A failing parser
  empty = Parser $ const Nothing

  (Parser p1) <|> (Parser p2) = Parser f
    where
      -- Here, we take advantage that Maybe is already Alternative
      f input = p1 input <|> p2 input

jsonBool :: Parser JsonValue
jsonBool = f <$> (stringP "true" <|> stringP "false")
  where
    f "true"  = JsonBool True
    f "false" = JsonBool False
    -- Should never happen!
    f _       = undefined

-- Here, we only know the class of the character, but not the actual characters.
-- We need some function to check the criteria of the character parsed.
-- (Char -> Bool) -> Parser String

-- In haskell, there's an interesting function called span which filters out chars
-- based on some criteria. Let's make something similar
-- span :: (Char -> Bool) -> [a] -> ([a], [a]) 

spanP :: (Char -> Bool) -> Parser String
spanP f = Parser f'
  where
    f' input =
      let (token, rest) = span f input
      in Just (rest, token)

-- We need to assure that the input is not empty. The jsonNumber parser will happily
-- accept empty inputs, and that's a problem

-- This parser combinator will convert a parser such that it should fail if the 
-- input is empty
notNull :: Parser [a] -> Parser [a]
notNull (Parser p) = Parser f
  where
    f input = do
      (input', xs) <- p input
      if null xs
        then Nothing
        else Just (input', xs)

jsonNumber :: Parser JsonValue
jsonNumber = f <$> notNull (spanP isDigit)
  where
    f digits = JsonNumber $ read digits

-- Note that this does not support escaping \"
stringLiteral :: Parser String
stringLiteral = charP '"' *> spanP (/='"') <* charP '"'

-- For string, we are going to need to parse quotation marks that are not going to be
-- part of the result value. For this, we have some functions from Applicative
-- that will help us.

-- (*>) :: f a -> f b -> f b
-- (<*) :: f a -> f b -> f a

-- These makes sure that f a, or f b is parsed, but returns only one of them.

jsonString :: Parser JsonValue
jsonString = JsonString <$> stringLiteral

whiteSpaceP :: Parser String
whiteSpaceP = spanP isSpace

-- Usually when working with parser combinators, we have this function called
-- "sepBy" that combines two parsers. a is used as a separator, while b is used as
-- an element. It combines into a parser that parses multiple elements, split by a

-- In Alternative, we have a function called
-- many :: Applicative f => f a -> f [a]

-- In this context, wrapping an Applicative Parser into many, will give you a Parser that
-- will parse elements into a list until it fails. Because we have defined the "empty" function,
-- Haskell know when it is a failed parser, and therefore it also knows when to stop.

sepBy :: Parser a -> Parser b -> Parser [b]
sepBy sep element =
  -- combine one parser with many other (sep + parser) parsers
  -- or parse it as an empty list.
  (:) <$> element <*> many (sep *> element)
  -- parser that will return [] and ignore the input
  <|> pure []

jsonArray :: Parser JsonValue
jsonArray = JsonArray <$> (charP '[' *> whiteSpaceP *> elements <* whiteSpaceP <* charP ']')
  where
    sep :: Parser Char
    sep = whiteSpaceP *> charP ',' <* whiteSpaceP

    elements :: Parser [JsonValue]
    elements = sepBy sep jsonValue

jsonObject :: Parser JsonValue
jsonObject = JsonObject <$> (charP '{' *> whiteSpaceP *> sepBy sep pair <* whiteSpaceP <* charP '}')
  where
    sep :: Parser Char
    sep = whiteSpaceP *> charP ',' <* whiteSpaceP

    -- pair :: Parser (String, JsonValue)
    pair =
      (\key _ value -> (key, value)) <$>
      stringLiteral <*> (whiteSpaceP *> charP ':' <* whiteSpaceP) <*> jsonValue

-- Combination of all the parsers
jsonValue :: Parser JsonValue
jsonValue = jsonNull <|> jsonBool <|> jsonNumber <|> jsonString <|> jsonArray <|> jsonObject

parseJson :: FilePath -> Maybe JsonValue
parseJson json = snd <$> runParser jsonValue json

-- parseFile :: FilePath -> IO JsonValue
-- parseFile fileName = do
--   readFile fileName >>= parseJson
parseFile :: String -> IO (Maybe JsonValue)
--                                (>>= return .)
parseFile fileName = readFile fileName <&> parseJson

main :: IO ()
main = do
  putStr "File to parse: "
  filePath <- getLine
  fileExists <- doesFileExist filePath
  if fileExists
    then parseFile filePath >>= print
    else putStrLn "No such file found!"