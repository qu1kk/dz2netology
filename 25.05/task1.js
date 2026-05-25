console.log('Синхронный код 1');

setTimeout(() => console.log('setTimeout 1'), 0);

Promise.resolve().then(() => console.log('Promise 1'));

console.log('Синхронный код 2');
