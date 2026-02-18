// ===== GLOBAL VARIABLES =====
let autoRefreshEnabled = true;
let refreshInterval = 2000;
let refreshTimer = null;
let charts = {};
let alerts = [];
let settings = {
    cpuThreshold: 85,
    ramThreshold: 90,
    diskThreshold: 95,
    refreshInterval: 2,
    enableNotifications: true,
    enableSounds: false,
    chartType: 'line',
    theme: 'default',
    showAnimations: true
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadSettings();
    setupEventListeners();
    startAutoRefresh();
    requestNotificationPermission();
});

function initializeApp() {
    // Hide loading overlay immediately
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
    
    updateLastUpdateTime();
    initializeCharts();
    loadInitialData();
}

function loadSettings() {
    const savedSettings = localStorage.getItem('dashboardSettings');
    if (savedSettings) {
        settings = { ...settings, ...JSON.parse(savedSettings) };
        applySettings();
    }
}

function applySettings() {
    refreshInterval = settings.refreshInterval * 1000;
    
    if (settings.theme === 'dark') {
        document.body.classList.add('dark-mode');
    }
    
    updateRefreshButton();
}

function saveSettings() {
    localStorage.setItem('dashboardSettings', JSON.stringify(settings));
    showToast('Settings saved successfully', 'success');
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    // Sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }
    
    if (mobileSidebarToggle) {
        mobileSidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }
    
    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }
    
    // Refresh button
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', manualRefresh);
    }
    
    // Auto refresh toggle
    const autoRefreshToggle = document.getElementById('autoRefreshToggle');
    if (autoRefreshToggle) {
        autoRefreshToggle.addEventListener('click', toggleAutoRefresh);
    }
    
    // Process refresh
    const refreshProcesses = document.getElementById('refreshProcesses');
    if (refreshProcesses) {
        refreshProcesses.addEventListener('click', loadProcesses);
    }
    
    // Settings page controls
    setupSettingsListeners();
    
    // Notification button
    const notificationBtn = document.getElementById('notificationBtn');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', showNotifications);
    }
}

function setupSettingsListeners() {
    // Threshold sliders
    const cpuThreshold = document.getElementById('cpuThreshold');
    const ramThreshold = document.getElementById('ramThreshold');
    const diskThreshold = document.getElementById('diskThreshold');
    
    if (cpuThreshold) {
        cpuThreshold.addEventListener('input', (e) => {
            settings.cpuThreshold = parseInt(e.target.value);
            document.getElementById('cpuThresholdValue').textContent = e.target.value + '%';
        });
    }
    
    if (ramThreshold) {
        ramThreshold.addEventListener('input', (e) => {
            settings.ramThreshold = parseInt(e.target.value);
            document.getElementById('ramThresholdValue').textContent = e.target.value + '%';
        });
    }
    
    if (diskThreshold) {
        diskThreshold.addEventListener('input', (e) => {
            settings.diskThreshold = parseInt(e.target.value);
            document.getElementById('diskThresholdValue').textContent = e.target.value + '%';
        });
    }
    
    // Refresh interval
    const refreshIntervalSelect = document.getElementById('refreshInterval');
    if (refreshIntervalSelect) {
        refreshIntervalSelect.addEventListener('change', (e) => {
            settings.refreshInterval = parseInt(e.target.value);
            refreshInterval = settings.refreshInterval * 1000;
            restartAutoRefresh();
        });
    }
    
    // Checkboxes
    const enableNotifications = document.getElementById('enableNotifications');
    const enableSounds = document.getElementById('enableSounds');
    const showAnimations = document.getElementById('showAnimations');
    
    if (enableNotifications) {
        enableNotifications.addEventListener('change', (e) => {
            settings.enableNotifications = e.target.checked;
        });
    }
    
    if (enableSounds) {
        enableSounds.addEventListener('change', (e) => {
            settings.enableSounds = e.target.checked;
        });
    }
    
    if (showAnimations) {
        showAnimations.addEventListener('change', (e) => {
            settings.showAnimations = e.target.checked;
            document.body.classList.toggle('no-animations', !e.target.checked);
        });
    }
    
    // Theme selector
    const themeSelect = document.getElementById('theme');
    if (themeSelect) {
        themeSelect.addEventListener('change', (e) => {
            settings.theme = e.target.value;
            applyTheme(e.target.value);
        });
    }
    
    // Save and reset buttons
    const saveSettingsBtn = document.getElementById('saveSettings');
    const resetSettingsBtn = document.getElementById('resetSettings');
    
    if (saveSettingsBtn) {
        saveSettingsBtn.addEventListener('click', saveSettings);
    }
    
    if (resetSettingsBtn) {
        resetSettingsBtn.addEventListener('click', resetSettings);
    }
}

// ===== CHARTS =====
function initializeCharts() {
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: settings.showAnimations ? 750 : 0
        },
        plugins: {
            legend: {
                display: false
            }
        }
    };
    
    // CPU Chart
    const cpuCtx = document.getElementById('cpuChart');
    if (cpuCtx) {
        charts.cpu = new Chart(cpuCtx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [0, 100],
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(226, 232, 240, 0.3)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                ...chartOptions,
                cutout: '70%'
            }
        });
    }
    
    // RAM Chart
    const ramCtx = document.getElementById('ramChart');
    if (ramCtx) {
        charts.ram = new Chart(ramCtx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [0, 100],
                    backgroundColor: [
                        'rgba(72, 187, 120, 0.8)',
                        'rgba(226, 232, 240, 0.3)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                ...chartOptions,
                cutout: '70%'
            }
        });
    }
    
    // Disk Chart
    const diskCtx = document.getElementById('diskChart');
    if (diskCtx) {
        charts.disk = new Chart(diskCtx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [0, 100],
                    backgroundColor: [
                        'rgba(246, 173, 85, 0.8)',
                        'rgba(226, 232, 240, 0.3)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                ...chartOptions,
                cutout: '70%'
            }
        });
    }
    
    // Network Chart
    const networkCtx = document.getElementById('networkChart');
    if (networkCtx) {
        charts.network = new Chart(networkCtx, {
            type: 'bar',
            data: {
                labels: ['Upload', 'Download'],
                datasets: [{
                    data: [0, 0],
                    backgroundColor: [
                        'rgba(66, 153, 225, 0.8)',
                        'rgba(159, 122, 234, 0.8)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                ...chartOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        display: false
                    },
                    x: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Performance History Chart
    const performanceCtx = document.getElementById('performanceChart');
    if (performanceCtx) {
        charts.performance = new Chart(performanceCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'CPU',
                        data: [],
                        borderColor: 'rgba(102, 126, 234, 1)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'RAM',
                        data: [],
                        borderColor: 'rgba(72, 187, 120, 1)',
                        backgroundColor: 'rgba(72, 187, 120, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Disk',
                        data: [],
                        borderColor: 'rgba(246, 173, 85, 1)',
                        backgroundColor: 'rgba(246, 173, 85, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                ...chartOptions,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
}

// ===== DATA LOADING =====
async function loadInitialData() {
    showLoading();
    try {
        await Promise.all([
            loadCPUMetrics(),
            loadRAMMetrics(),
            loadDiskMetrics(),
            loadNetworkMetrics(),
            loadSystemInfo(),
            loadProcesses(),
            loadAlerts()
        ]);
    } catch (error) {
        console.error('Error loading initial data:', error);
        showToast('Failed to load system metrics', 'error');
    } finally {
        hideLoading();
    }
}

async function loadCPUMetrics() {
    try {
        const response = await fetch('/api/cpu');
        const data = await response.json();
        
        updateCPUChart(data.percentage);
        updateCPUInfo(data);
    } catch (error) {
        console.error('Error loading CPU metrics:', error);
    }
}

async function loadRAMMetrics() {
    try {
        const response = await fetch('/api/ram');
        const data = await response.json();
        
        updateRAMChart(data.percentage);
        updateRAMInfo(data);
    } catch (error) {
        console.error('Error loading RAM metrics:', error);
    }
}

async function loadDiskMetrics() {
    try {
        const response = await fetch('/api/disk');
        const data = await response.json();
        
        updateDiskChart(data.percentage);
        updateDiskInfo(data);
    } catch (error) {
        console.error('Error loading Disk metrics:', error);
    }
}

async function loadNetworkMetrics() {
    try {
        const response = await fetch('/api/network');
        const data = await response.json();
        
        updateNetworkChart(data);
        updateNetworkInfo(data);
    } catch (error) {
        console.error('Error loading Network metrics:', error);
    }
}

async function loadSystemInfo() {
    try {
        const response = await fetch('/api/system-info');
        const data = await response.json();
        
        updateSystemInfo(data);
    } catch (error) {
        console.error('Error loading System info:', error);
    }
}

async function loadProcesses() {
    try {
        const response = await fetch('/api/processes');
        const data = await response.json();
        
        updateProcessesTable(data);
    } catch (error) {
        console.error('Error loading processes:', error);
    }
}

async function loadAlerts() {
    try {
        const response = await fetch('/api/alerts');
        const data = await response.json();
        
        updateAlerts(data);
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}

// ===== UPDATE FUNCTIONS =====
function updateCPUChart(percentage) {
    if (charts.cpu) {
        charts.cpu.data.datasets[0].data = [percentage, 100 - percentage];
        charts.cpu.update();
    }
    
    const cpuValue = document.getElementById('cpuValue');
    if (cpuValue) {
        cpuValue.textContent = percentage.toFixed(1) + '%';
    }
    
    updatePerformanceHistory('cpu', percentage);
}

function updateCPUInfo(data) {
    const cpuCores = document.getElementById('cpuCores');
    const cpuFreq = document.getElementById('cpuFreq');
    
    if (cpuCores) {
        cpuCores.textContent = data.cores || '-';
    }
    
    if (cpuFreq && data.frequency) {
        cpuFreq.textContent = (data.frequency.current / 1000).toFixed(1) + ' GHz';
    }
}

function updateRAMChart(percentage) {
    if (charts.ram) {
        charts.ram.data.datasets[0].data = [percentage, 100 - percentage];
        charts.ram.update();
    }
    
    const ramValue = document.getElementById('ramValue');
    if (ramValue) {
        ramValue.textContent = percentage.toFixed(1) + '%';
    }
    
    updatePerformanceHistory('ram', percentage);
}

function updateRAMInfo(data) {
    const ramTotal = document.getElementById('ramTotal');
    const ramAvailable = document.getElementById('ramAvailable');
    
    if (ramTotal) {
        ramTotal.textContent = formatBytes(data.total);
    }
    
    if (ramAvailable) {
        ramAvailable.textContent = formatBytes(data.available);
    }
}

function updateDiskChart(percentage) {
    if (charts.disk) {
        charts.disk.data.datasets[0].data = [percentage, 100 - percentage];
        charts.disk.update();
    }
    
    const diskValue = document.getElementById('diskValue');
    if (diskValue) {
        diskValue.textContent = percentage.toFixed(1) + '%';
    }
    
    updatePerformanceHistory('disk', percentage);
}

function updateDiskInfo(data) {
    const diskTotal = document.getElementById('diskTotal');
    const diskFree = document.getElementById('diskFree');
    
    if (diskTotal) {
        diskTotal.textContent = formatBytes(data.total);
    }
    
    if (diskFree) {
        diskFree.textContent = formatBytes(data.free);
    }
}

function updateNetworkChart(data) {
    if (charts.network) {
        charts.network.data.datasets[0].data = [
            formatSpeed(data.upload_speed),
            formatSpeed(data.download_speed)
        ];
        charts.network.update();
    }
}

function updateNetworkInfo(data) {
    const networkUpload = document.getElementById('networkUpload');
    const networkDownload = document.getElementById('networkDownload');
    
    if (networkUpload) {
        networkUpload.textContent = formatSpeed(data.upload_speed) + '/s';
    }
    
    if (networkDownload) {
        networkDownload.textContent = formatSpeed(data.download_speed) + '/s';
    }
}

function updateSystemInfo(data) {
    const systemUptime = document.getElementById('systemUptime');
    const bootTime = document.getElementById('bootTime');
    
    if (systemUptime) {
        systemUptime.textContent = data.uptime_formatted;
    }
    
    if (bootTime) {
        bootTime.textContent = data.boot_time;
    }
}

function updateProcessesTable(processes) {
    const tbody = document.getElementById('processesTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    processes.forEach(process => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${process.pid}</td>
            <td>${process.name}</td>
            <td>${process.cpu_percent.toFixed(1)}%</td>
            <td>${process.memory_percent.toFixed(1)}%</td>
            <td><span class="badge bg-${getStatusColor(process.status)}">${process.status}</span></td>
        `;
        tbody.appendChild(row);
    });
}

function updateAlerts(alertData) {
    alerts = alertData;
    const alertsSection = document.getElementById('alertsSection');
    const notificationBadge = document.getElementById('notificationBadge');
    
    if (!alertsSection) return;
    
    alertsSection.innerHTML = '';
    
    if (alerts.length === 0) {
        alertsSection.style.display = 'none';
        if (notificationBadge) {
            notificationBadge.textContent = '0';
            notificationBadge.style.display = 'none';
        }
        return;
    }
    
    alertsSection.style.display = 'block';
    
    alerts.forEach(alert => {
        const alertElement = createAlertElement(alert);
        alertsSection.appendChild(alertElement);
    });
    
    if (notificationBadge) {
        notificationBadge.textContent = alerts.length;
        notificationBadge.style.display = alerts.length > 0 ? 'block' : 'none';
    }
    
    if (settings.enableNotifications) {
        alerts.forEach(alert => {
            if (alert.severity === 'critical') {
                showBrowserNotification(alert.message, alert.severity);
            }
        });
    }
}

function createAlertElement(alert) {
    const div = document.createElement('div');
    div.className = `alert-item ${alert.severity}`;
    div.innerHTML = `
        <div class="alert-content">
            <div class="alert-icon">
                <i class="fas fa-${getAlertIcon(alert.severity)}"></i>
            </div>
            <div class="alert-message">${alert.message}</div>
            <div class="alert-time">${formatTime(alert.created_at)}</div>
        </div>
        <div class="alert-actions">
            <button class="alert-btn alert-resolve" onclick="resolveAlert(${alert.id})">
                Resolve
            </button>
        </div>
    `;
    return div;
}

async function resolveAlert(alertId) {
    try {
        const response = await fetch(`/api/resolve-alert/${alertId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            loadAlerts();
            showToast('Alert resolved', 'success');
        }
    } catch (error) {
        console.error('Error resolving alert:', error);
        showToast('Failed to resolve alert', 'error');
    }
}

function updatePerformanceHistory(type, value) {
    if (!charts.performance) return;
    
    const now = new Date();
    const timeLabel = now.toLocaleTimeString();
    
    // Add new data point
    if (charts.performance.data.labels.length === 0 || 
        charts.performance.data.labels[charts.performance.data.labels.length - 1] !== timeLabel) {
        
        charts.performance.data.labels.push(timeLabel);
        
        // Add data to appropriate dataset
        const datasetIndex = type === 'cpu' ? 0 : type === 'ram' ? 1 : 2;
        charts.performance.data.datasets[datasetIndex].data.push(value);
        
        // Keep only last 20 data points
        if (charts.performance.data.labels.length > 20) {
            charts.performance.data.labels.shift();
            charts.performance.data.datasets.forEach(dataset => {
                dataset.data.shift();
            });
        }
        
        charts.performance.update();
    }
}

// ===== AUTO REFRESH =====
function startAutoRefresh() {
    if (autoRefreshEnabled) {
        refreshTimer = setInterval(() => {
            refreshData();
        }, refreshInterval);
    }
}

function stopAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
    }
}

function restartAutoRefresh() {
    stopAutoRefresh();
    startAutoRefresh();
}

function toggleAutoRefresh() {
    autoRefreshEnabled = !autoRefreshEnabled;
    const btn = document.getElementById('autoRefreshToggle');
    
    if (autoRefreshEnabled) {
        startAutoRefresh();
        btn.innerHTML = '<i class="fas fa-play"></i> Auto Refresh: ON';
        btn.classList.remove('btn-secondary');
        btn.classList.add('btn-primary');
    } else {
        stopAutoRefresh();
        btn.innerHTML = '<i class="fas fa-pause"></i> Auto Refresh: OFF';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
    }
}

function manualRefresh() {
    showLoading();
    refreshData().finally(() => {
        hideLoading();
        showToast('Data refreshed successfully', 'success');
    });
}

async function refreshData() {
    try {
        await Promise.all([
            loadCPUMetrics(),
            loadRAMMetrics(),
            loadDiskMetrics(),
            loadNetworkMetrics(),
            loadSystemInfo(),
            loadAlerts()
        ]);
        updateLastUpdateTime();
    } catch (error) {
        console.error('Error refreshing data:', error);
    }
}

function updateLastUpdateTime() {
    const lastUpdate = document.getElementById('lastUpdate');
    if (lastUpdate) {
        lastUpdate.textContent = new Date().toLocaleTimeString();
    }
}

// ===== UI FUNCTIONS =====
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    settings.theme = isDarkMode ? 'dark' : 'default';
    saveSettings();
    
    const darkModeToggle = document.getElementById('darkModeToggle');
    const icon = darkModeToggle.querySelector('i');
    icon.className = isDarkMode ? 'fas fa-sun' : 'fas fa-moon';
}

function applyTheme(theme) {
    document.body.classList.remove('dark-mode');
    
    switch (theme) {
        case 'dark':
            document.body.classList.add('dark-mode');
            break;
        case 'green':
            document.documentElement.style.setProperty('--primary-color', '#48bb78');
            document.documentElement.style.setProperty('--secondary-color', '#38a169');
            break;
        case 'purple':
            document.documentElement.style.setProperty('--primary-color', '#9f7aea');
            document.documentElement.style.setProperty('--secondary-color', '#805ad5');
            break;
        default:
            document.documentElement.style.setProperty('--primary-color', '#667eea');
            document.documentElement.style.setProperty('--secondary-color', '#764ba2');
    }
}

function resetSettings() {
    if (confirm('Are you sure you want to reset all settings to default?')) {
        settings = {
            cpuThreshold: 85,
            ramThreshold: 90,
            diskThreshold: 95,
            refreshInterval: 2,
            enableNotifications: true,
            enableSounds: false,
            chartType: 'line',
            theme: 'default',
            showAnimations: true
        };
        
        localStorage.removeItem('dashboardSettings');
        location.reload();
    }
}

function showNotifications() {
    // Show current alerts in a modal or dropdown
    if (alerts.length === 0) {
        showToast('No active notifications', 'info');
    } else {
        let message = `You have ${alerts.length} active alert${alerts.length > 1 ? 's' : ''}:\n\n`;
        alerts.forEach((alert, index) => {
            message += `${index + 1}. ${alert.message}\n`;
        });
        showToast(message, 'warning');
    }
}

// ===== UTILITY FUNCTIONS =====
function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function formatSpeed(bytesPerSecond) {
    return formatBytes(bytesPerSecond);
}

function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString();
}

function getStatusColor(status) {
    switch (status.toLowerCase()) {
        case 'running':
            return 'success';
        case 'sleeping':
            return 'info';
        case 'idle':
            return 'secondary';
        default:
            return 'warning';
    }
}

function getAlertIcon(severity) {
    switch (severity) {
        case 'critical':
            return 'exclamation-circle';
        case 'warning':
            return 'exclamation-triangle';
        case 'info':
            return 'info-circle';
        default:
            return 'info-circle';
    }
}

function showLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('active');
    }
}

function hideLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('active');
    }
}

function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-header">
            <span class="toast-title">${type.charAt(0).toUpperCase() + type.slice(1)}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="toast-body">${message}</div>
    `;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

function showBrowserNotification(message, severity = 'info') {
    if ('Notification' in window && Notification.permission === 'granted' && settings.enableNotifications) {
        const notification = new Notification('Network Monitor Alert', {
            body: message,
            icon: '/static/images/icon.png',
            badge: '/static/images/badge.png'
        });
        
        notification.onclick = function() {
            window.focus();
            notification.close();
        };
        
        setTimeout(() => {
            notification.close();
        }, 5000);
    }
}

function updateRefreshButton() {
    const btn = document.getElementById('autoRefreshToggle');
    if (btn) {
        if (autoRefreshEnabled) {
            btn.innerHTML = '<i class="fas fa-play"></i> Auto Refresh: ON';
            btn.classList.remove('btn-secondary');
            btn.classList.add('btn-primary');
        } else {
            btn.innerHTML = '<i class="fas fa-pause"></i> Auto Refresh: OFF';
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-secondary');
        }
    }
}

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + R: Manual refresh
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        manualRefresh();
    }
    
    // Ctrl/Cmd + D: Toggle dark mode
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        toggleDarkMode();
    }
    
    // Escape: Close sidebar on mobile
    if (e.key === 'Escape') {
        const sidebar = document.getElementById('sidebar');
        if (sidebar && sidebar.classList.contains('active')) {
            sidebar.classList.remove('active');
        }
    }
});

// ===== WINDOW RESIZE HANDLER =====
window.addEventListener('resize', function() {
    // Handle responsive chart resizing
    Object.values(charts).forEach(chart => {
        if (chart) {
            chart.resize();
        }
    });
});

// ===== BEFORE UNLOAD =====
window.addEventListener('beforeunload', function() {
    stopAutoRefresh();
});
