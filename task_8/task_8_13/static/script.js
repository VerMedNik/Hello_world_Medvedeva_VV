const statsOutput = document.getElementById('stats-output');
const chartCanvas = document.getElementById('chart-canvas');
const statusMessage = document.getElementById('status-message');
let currentChart = null;

const API_ENDPOINTS = {
    average: '/api/data/average',
    median: '/api/data/median',
    count: '/api/data/count',
    'bar-chart': '/api/data/bar-chart',
    'pie-chart': '/api/data/pie-chart'
};

function showLoading() {
    statusMessage.textContent = 'Загрузка...';
    statusMessage.className = 'loading';
    statsOutput.innerHTML = '';
}

function showError(message) {
    statusMessage.textContent = message;
    statusMessage.className = 'error';
}

function clearContent() {
    statsOutput.innerHTML = '';
    if (currentChart) {
        currentChart.destroy();
        currentChart = null;
    }
    statusMessage.innerHTML = '';
}

async function fetchData(endpoint) {
    showLoading();
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.error) {
            showError(data.error);
            return null;
        }
        return data;
    } catch (error) {
        showError('Ошибка при запросе к серверу: ' + error.message);
        return null;
    }
}

function renderStats(value) {
    statsOutput.innerHTML = `<p><strong>Результат:</strong> ${value.toFixed(2)}</p>`;
    statusMessage.innerHTML = '';
}

function renderBarChart(labels, values, metric) {
    if (currentChart) {
        currentChart.destroy();
    }
    const ctx = chartCanvas.getContext('2d');
    currentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Среднее значение по группам',
                data: values,
                backgroundColor: 'rgba(52, 152, 219, 0.7)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Значение'
                    }
                }
            },
            plugins: {
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: metric,
                            yMax: metric,
                            borderColor: 'rgb(231, 76, 60)',
                            borderWidth: 2,
                            label: {
                                content: `Среднее: ${metric.toFixed(2)}`,
                                enabled: true,
                                position: 'start'
                            }
                        }
                    }
                }
            }
        }
    });
    statusMessage.innerHTML = '';
}

function renderPieChart(labels, values) {
    if (currentChart) {
        currentChart.destroy();
    }
    const ctx = chartCanvas.getContext('2d');
    currentChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    'rgba(231, 76, 60, 0.7)',
                    'rgba(46, 204, 113, 0.7)',
                    'rgba(52, 152, 219, 0.7)',
                    'rgba(155, 89, 182, 0.7)',
                    'rgba(241, 196, 15, 0.7)'
                ],
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
    statusMessage.innerHTML = '';
}

document.querySelectorAll('.sidebar-btn').forEach(button => {
    button.addEventListener('click', async (event) => {
        const action = event.target.getAttribute('data-action');
        if (action === 'clear') {
            clearContent();
            return;
        }

        const endpoint = API_ENDPOINTS[action];
        if (!endpoint) return;

        const data = await fetchData(endpoint);
        if (!data) return;

        if (action === 'average' || action === 'median' || action === 'count') {
            renderStats(data.value);
        } else if (action === 'bar-chart') {
            renderBarChart(data.labels, data.values, data.metric);
        } else if (action === 'pie-chart') {
            renderPieChart(data.labels, data.values);
        }
    });
});

document.getElementById('clear-btn').addEventListener('click', clearContent);
