// ProspectPlusAgent JavaScript Application

const API_BASE = '/api';

// State management
const state = {
    prospects: [],
    currentTab: 'dashboard',
    filters: {
        status: '',
        priority: ''
    }
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadDashboard();
    checkAgentStatus();
});

// Event Listeners
function initializeEventListeners() {
    // Tab navigation
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Add prospect button
    document.getElementById('add-prospect-btn').addEventListener('click', openAddProspectModal);

    // Modal close buttons
    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', closeModals);
    });

    // Add prospect form
    document.getElementById('add-prospect-form').addEventListener('submit', handleAddProspect);

    // Chat functionality
    document.getElementById('send-chat-btn').addEventListener('click', sendChatMessage);
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });

    // Filters
    document.getElementById('status-filter').addEventListener('change', (e) => {
        state.filters.status = e.target.value;
        loadProspects();
    });

    document.getElementById('priority-filter').addEventListener('change', (e) => {
        state.filters.priority = e.target.value;
        loadProspects();
    });

    // Close modal on outside click
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            closeModals();
        }
    });
}

// Tab switching
function switchTab(tabName) {
    state.currentTab = tabName;

    // Update tab buttons
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === tabName);
    });

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === tabName);
    });

    // Load data for the tab
    switch (tabName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'prospects':
            loadProspects();
            break;
        case 'analytics':
            loadAnalytics();
            break;
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const [analytics, prospects] = await Promise.all([
            fetch(`${API_BASE}/analytics/overview`).then(r => r.json()),
            fetch(`${API_BASE}/prospects?limit=5`).then(r => r.json())
        ]);

        // Update stats
        document.getElementById('total-prospects').textContent = analytics.total_prospects;
        document.getElementById('qualified-prospects').textContent = 
            analytics.by_status.qualified || 0;
        document.getElementById('high-priority').textContent = 
            (analytics.by_priority.high || 0) + (analytics.by_priority.critical || 0);
        document.getElementById('conversion-rate').textContent = 
            `${(analytics.conversion_rate * 100).toFixed(1)}%`;

        // Display recent prospects
        displayRecentProspects(prospects);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showError('Failed to load dashboard data');
    }
}

function displayRecentProspects(prospects) {
    const container = document.getElementById('recent-prospects-list');
    
    if (prospects.length === 0) {
        container.innerHTML = '<p class="loading">No prospects yet. Add your first prospect!</p>';
        return;
    }

    container.innerHTML = prospects.map(prospect => `
        <div class="prospect-card">
            <div class="prospect-header">
                <div>
                    <div class="prospect-name">${escapeHtml(prospect.contact_name)}</div>
                    <div class="prospect-company">${escapeHtml(prospect.company_name)}</div>
                </div>
                <div>
                    <span class="badge badge-${prospect.status}">${prospect.status}</span>
                </div>
            </div>
            <div class="prospect-details">
                <span><i class="fas fa-envelope"></i> ${escapeHtml(prospect.email)}</span>
                ${prospect.industry ? `<span><i class="fas fa-industry"></i> ${escapeHtml(prospect.industry)}</span>` : ''}
                <span class="badge badge-${prospect.priority}">${prospect.priority}</span>
            </div>
        </div>
    `).join('');
}

// Prospects
async function loadProspects() {
    const container = document.getElementById('prospects-list');
    container.innerHTML = '<p class="loading">Loading prospects...</p>';

    try {
        let url = `${API_BASE}/prospects?limit=100`;
        if (state.filters.status) url += `&status=${state.filters.status}`;
        if (state.filters.priority) url += `&priority=${state.filters.priority}`;

        const prospects = await fetch(url).then(r => r.json());
        state.prospects = prospects;

        if (prospects.length === 0) {
            container.innerHTML = '<p class="loading">No prospects found. Try adjusting your filters or add a new prospect.</p>';
            return;
        }

        container.innerHTML = prospects.map(prospect => `
            <div class="prospect-card">
                <div class="prospect-header">
                    <div>
                        <div class="prospect-name">${escapeHtml(prospect.contact_name)}</div>
                        <div class="prospect-company">${escapeHtml(prospect.company_name)}</div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <span class="badge badge-${prospect.status}">${prospect.status}</span>
                        <span class="badge badge-${prospect.priority}">${prospect.priority}</span>
                    </div>
                </div>
                <div class="prospect-details">
                    <span><i class="fas fa-envelope"></i> ${escapeHtml(prospect.email)}</span>
                    ${prospect.phone ? `<span><i class="fas fa-phone"></i> ${escapeHtml(prospect.phone)}</span>` : ''}
                    ${prospect.industry ? `<span><i class="fas fa-industry"></i> ${escapeHtml(prospect.industry)}</span>` : ''}
                    ${prospect.score ? `<span><i class="fas fa-star"></i> Score: ${(prospect.score * 100).toFixed(0)}%</span>` : ''}
                </div>
                ${prospect.notes ? `<p style="margin-top: 8px; color: #6b7280; font-size: 0.9rem;">${escapeHtml(prospect.notes)}</p>` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading prospects:', error);
        container.innerHTML = '<p class="loading">Error loading prospects. Please try again.</p>';
    }
}

// Modal functions
function openAddProspectModal() {
    document.getElementById('add-prospect-modal').classList.add('active');
}

function closeModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('active');
    });
    document.getElementById('add-prospect-form').reset();
}

async function handleAddProspect(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const prospectData = {
        company_name: formData.get('company_name'),
        contact_name: formData.get('contact_name'),
        email: formData.get('email'),
        phone: formData.get('phone') || null,
        industry: formData.get('industry') || null,
        company_size: formData.get('company_size') || null,
        website: formData.get('website') || null,
        status: formData.get('status'),
        priority: formData.get('priority'),
        notes: formData.get('notes') || null,
        tags: []
    };

    try {
        const response = await fetch(`${API_BASE}/prospects/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(prospectData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create prospect');
        }

        const newProspect = await response.json();
        showSuccess('Prospect added successfully!');
        closeModals();
        
        // Reload current view
        if (state.currentTab === 'prospects') {
            loadProspects();
        } else {
            loadDashboard();
        }
    } catch (error) {
        console.error('Error adding prospect:', error);
        showError(error.message);
    }
}

// Agent Chat
async function checkAgentStatus() {
    try {
        const status = await fetch(`${API_BASE}/agent/status`).then(r => r.json());
        const statusElement = document.getElementById('agent-status');
        
        if (status.ai_enabled) {
            statusElement.querySelector('.status-text').textContent = 'AI Enabled';
            statusElement.querySelector('.status-indicator').style.background = '#10b981';
        } else {
            statusElement.querySelector('.status-text').textContent = 'Limited Mode';
            statusElement.querySelector('.status-indicator').style.background = '#f59e0b';
        }
    } catch (error) {
        console.error('Error checking agent status:', error);
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;

    const chatContainer = document.getElementById('chat-container');
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
        const response = await fetch(`${API_BASE}/agent/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: message })
        });

        const data = await response.json();
        
        // Remove typing indicator
        document.getElementById(typingId)?.remove();
        
        // Add assistant response
        addChatMessage(data.response, 'assistant');
    } catch (error) {
        console.error('Error sending chat message:', error);
        document.getElementById(typingId)?.remove();
        addChatMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    }
}

function addChatMessage(message, type) {
    const chatContainer = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}`;
    
    const icon = type === 'assistant' ? 
        '<i class="fas fa-robot"></i>' : 
        '<i class="fas fa-user"></i>';
    
    messageDiv.innerHTML = `
        <div class="message-icon">${icon}</div>
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addTypingIndicator() {
    const chatContainer = document.getElementById('chat-container');
    const id = `typing-${Date.now()}`;
    const typingDiv = document.createElement('div');
    typingDiv.id = id;
    typingDiv.className = 'chat-message assistant';
    typingDiv.innerHTML = `
        <div class="message-icon"><i class="fas fa-robot"></i></div>
        <div class="message-content">
            <p><i class="fas fa-circle-notch fa-spin"></i> Thinking...</p>
        </div>
    `;
    
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return id;
}

// Analytics
async function loadAnalytics() {
    try {
        const [overview, industries] = await Promise.all([
            fetch(`${API_BASE}/analytics/overview`).then(r => r.json()),
            fetch(`${API_BASE}/analytics/top-industries`).then(r => r.json())
        ]);

        // Display status chart (simple bar representation)
        displayStatusChart(overview.by_status);
        
        // Display priority chart
        displayPriorityChart(overview.by_priority);
        
        // Display industries
        displayIndustries(industries.industries);
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

function displayStatusChart(byStatus) {
    const canvas = document.getElementById('statusCanvas');
    const ctx = canvas.getContext('2d');
    
    // Simple bar chart
    const data = Object.entries(byStatus);
    const max = Math.max(...data.map(([_, count]) => count), 1);
    
    canvas.width = 400;
    canvas.height = 250;
    
    const barWidth = canvas.width / data.length;
    const colors = ['#3b82f6', '#f59e0b', '#10b981', '#8b5cf6', '#ec4899', '#10b981', '#ef4444'];
    
    data.forEach(([status, count], index) => {
        const height = (count / max) * (canvas.height - 40);
        const x = index * barWidth + 10;
        const y = canvas.height - height - 20;
        
        ctx.fillStyle = colors[index % colors.length];
        ctx.fillRect(x, y, barWidth - 20, height);
        
        ctx.fillStyle = '#374151';
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(count, x + (barWidth - 20) / 2, y - 5);
        ctx.fillText(status, x + (barWidth - 20) / 2, canvas.height - 5);
    });
}

function displayPriorityChart(byPriority) {
    const canvas = document.getElementById('priorityCanvas');
    const ctx = canvas.getContext('2d');
    
    const data = Object.entries(byPriority);
    const max = Math.max(...data.map(([_, count]) => count), 1);
    
    canvas.width = 400;
    canvas.height = 250;
    
    const barWidth = canvas.width / data.length;
    const colors = ['#9ca3af', '#3b82f6', '#f59e0b', '#ef4444'];
    
    data.forEach(([priority, count], index) => {
        const height = (count / max) * (canvas.height - 40);
        const x = index * barWidth + 10;
        const y = canvas.height - height - 20;
        
        ctx.fillStyle = colors[index % colors.length];
        ctx.fillRect(x, y, barWidth - 20, height);
        
        ctx.fillStyle = '#374151';
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(count, x + (barWidth - 20) / 2, y - 5);
        ctx.fillText(priority, x + (barWidth - 20) / 2, canvas.height - 5);
    });
}

function displayIndustries(industries) {
    const container = document.getElementById('industries-list');
    
    if (industries.length === 0) {
        container.innerHTML = '<p class="loading">No industry data available</p>';
        return;
    }
    
    container.innerHTML = industries.map(industry => `
        <div class="industry-item">
            <span style="font-weight: 500;">${escapeHtml(industry.name)}</span>
            <span style="color: #6b7280;">${industry.count} prospects</span>
        </div>
    `).join('');
}

// Utility functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showSuccess(message) {
    // Simple alert for now - could be replaced with a toast notification
    alert(message);
}

function showError(message) {
    // Simple alert for now - could be replaced with a toast notification
    alert('Error: ' + message);
}
