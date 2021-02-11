const curry = (func, ...args) => {
  return (...next) => {
    // By returning a function to be executed, you are
    // storing the state of the arguments in the curry constructor
    // by appending ...next to ...args.
    // use "curriedFunc()" when ready to execute after last argument has been added
    // (then next.length will be 0)
    const nextArgumentExists = next.length != 0;
    return nextArgumentExists
         ? curry(func, ...args, ...next)
         : func(...args);
  }
}

const exampleFunc = (a, b, c) => a + b + c;

console.log(curry(exampleFunc)(1)(2)(3)());

const curriedFunction = curry(exampleFunc)(5)(7);
console.log(curriedFunction(8)());
console.log(curriedFunction(9)());

const currySafe = (func, ...args) => {
  return (...next) => {
    if (next.length != 0) {
      return currySafe(func, ...args, ...next);
    } else {
      if (next.length == 0 && args.length != func.length)
        throw Error(
          `Argument count doesn\'t match
          [Expected]: ${func.length}
          [ArgumentCount]: ${args.length}`
          );
      return func(...args);
    }
  }
}
try {
  console.log(currySafe(exampleFunc)(2)(4)(8)());
  console.log(currySafe(exampleFunc)(2)(4)());
} catch (error) {
  console.log(error.message);
}