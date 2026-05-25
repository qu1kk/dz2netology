// Функция для создания задержки
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Модифицированная функция имитации API
async function fetchAsyncData(url) {
  await delay(2000);
  
  if (url === '/api/users') {
    return ['Ivan', 'Maria', 'Alex'];
  } else if (url.startsWith('/api/users/')) {
    const userName = url.split('/').pop();
    return { name: userName, age: 25, status: 'Active' };
  } else {
    throw new Error(`Ошибка 404: Ресурс ${url} не найден`);
  }
}

// Главная асинхронная функция
async function loadUserData() {
  console.log('Запуск Задания 3: Загрузка данных через async/await...');
  
  try {
    const users = await fetchAsyncData('/api/users');
    console.log('1. Получен список пользователей (async):', users);
    
    const firstUser = users[0];
    
    const userInfo = await fetchAsyncData(`/api/users/${firstUser}`);
    console.log('2. Информация о первом пользователе (async):', userInfo);
    
    
  } catch (error) {
    console.error('Произошла ошибка (try...catch):', error.message);
  }
}

loadUserData();