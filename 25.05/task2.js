// Функция, возвращающая Promise с задержкой 2 секунды
function fetchData(url) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (url === '/api/users') {
        resolve(['Ivan', 'Maria', 'Alex']); 
      } else if (url.startsWith('/api/users/')) {
        const userName = url.split('/').pop();
        resolve({ name: userName, age: 25, status: 'Active' }); 
      } else {
        reject(new Error(`Ошибка 404: Ресурс ${url} не найден`));
      }
    }, 2000);
  });
}

// Цепочка вызовов
console.log('Запуск Задания 2: Загрузка данных...');

fetchData('/api/users')
  .then((users) => {
    console.log('1. Получен список пользователей:', users);
    const firstUser = users[0]; 
    
    return fetchData(`/api/users/${firstUser}`);
  })
  .then((userInfo) => {
    console.log('2. Информация о первом пользователе:', userInfo);
  })
  .catch((error) => {
    // Обработка любых ошибок в цепочке
    console.error('Произошла ошибка во время запросов:', error.message);
  });