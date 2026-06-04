/**
 * Веб-приложение для анализа базы данных student_task
 * Обрабатывает клики по кнопкам, отправляет fetch-запросы на сервер,
 * отображает результаты (числа и графики) без перезагрузки страницы
 */

// Константы
const API_BASE = '';  // пустая строка, так как пути относительные
const resultArea = document.getElementById('result-area');

/**
 * Показывает состояние загрузки
 */
function showLoading() {
    resultArea.innerHTML = `
        <div class="loading">
            Загрузка данных...
        </div>
    `;
}

/**
 * Показывает сообщение об ошибке
 * @param {string} message - текст ошибки
 */
function showError(message) {
    resultArea.innerHTML = `
        <div class="error">
            ❌ Ошибка: ${message}
        </div>
    `;
}

/**
 * Отображает статистическую карточку (число)
 * @param {Object} data - данные от сервера
 */
function displayStat(data) {
    resultArea.innerHTML = `
        <div class="stat-card">
            <div class="label">${data.label}</div>
            <div class="value">${data.value}</div>
            <div class="description">${data.description || 'Статистическая метрика'}</div>
        </div>
    `;
}

/**
 * Отображает график
 * @param {Object} data - данные от сервера (содержат base64-изображение)
 */
function displayChart(data) {
    let statsHtml = '';
    if (data.stats) {
        statsHtml = `
            <div class="chart-stats">
                📊 Статистика на графике: 
                ${Object.entries(data.stats).map(([key, val]) => `<span>${key}: ${val}</span>`).join(' · ')}
            </div>
        `;
    }
    
    resultArea.innerHTML = `
        <div class="chart-container">
            <img src="data:image/png;base64,${data.image}" alt="График">
            ${statsHtml}
        </div>
    `;
}

/**
 * Возвращает URL для статистического запроса
 * @param {string} metric - метрика (mean, median, total, std, min, max)
 * @returns {string}
 */
function getStatUrl(metric) {
    const endpoints = {
        mean: '/api/metric/mean',
        median: '/api/metric/median',
        total: '/api/metric/total',
        std: '/api/metric/std',
        min: '/api/metric/min',
        max: '/api/metric/max'
    };
    return endpoints[metric] || endpoints.mean;
}

/**
 * Возвращает URL для запроса графика
 * @param {string} kind - тип графика (histogram, courses)
 * @returns {string}
 */
function getChartUrl(kind) {
    const endpoints = {
        histogram: '/api/chart/histogram',
        courses: '/api/chart/courses'
    };
    return endpoints[kind] || endpoints.histogram;
}

/**
 * Загружает статистические данные с сервера
 * @param {string} metric - метрика
 */
async function loadStat(metric) {
    showLoading();
    const url = getStatUrl(metric);
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            displayStat(data);
        } else {
            showError(data.error || 'Неизвестная ошибка');
        }
    } catch (error) {
        console.error('Ошибка запроса:', error);
        showError('Не удалось подключиться к серверу. Убедитесь, что Flask запущен.');
    }
}

/**
 * Загружает график с сервера
 * @param {string} kind - тип графика
 */
async function loadChart(kind) {
    showLoading();
    const url = getChartUrl(kind);
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            displayChart(data);
        } else {
            showError(data.error || 'Не удалось построить график');
        }
    } catch (error) {
        console.error('Ошибка запроса:', error);
        showError('Не удалось подключиться к серверу. Убедитесь, что Flask запущен.');
    }
}

/**
 * Очищает область результатов
 */
function clearResult() {
    resultArea.innerHTML = `
        <div class="placeholder">
            ← Нажмите кнопку слева, чтобы увидеть результат
        </div>
    `;
}

/**
 * Обработчик кликов по кнопкам
 * @param {Event} event
 */
function handleButtonClick(event) {
    const button = event.currentTarget;
    const action = button.dataset.action;
    
    if (action === 'stat') {
        const metric = button.dataset.metric;
        loadStat(metric);
    } else if (action === 'chart') {
        const kind = button.dataset.kind;
        loadChart(kind);
    }
}

/**
 * Инициализация приложения
 */
function init() {
    // Находим все кнопки с data-action
    const statButtons = document.querySelectorAll('.action-btn[data-action="stat"]');
    const chartButtons = document.querySelectorAll('.action-btn[data-action="chart"]');
    const clearButton = document.getElementById('clear-btn');
    
    // Добавляем обработчики для статистических кнопок
    statButtons.forEach(btn => {
        btn.addEventListener('click', handleButtonClick);
    });
    
    // Добавляем обработчики для кнопок графиков
    chartButtons.forEach(btn => {
        btn.addEventListener('click', handleButtonClick);
    });
    
    // Добавляем обработчик для кнопки очистки
    if (clearButton) {
        clearButton.addEventListener('click', clearResult);
    }
    
    console.log('✅ Приложение инициализировано');
}

// Запускаем инициализацию после полной загрузки DOM
document.addEventListener('DOMContentLoaded', init);