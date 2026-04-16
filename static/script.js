/**
 * Intelligent Feedback Analysis System
 * Frontend JavaScript - API calls, tab switching, charts, interactions
 */

// ============ STATE ============
let currentTab = 'home';
let generatedText = '';
let pieChart = null;
let barChart = null;

// Determine API Base URL dynamically
// If opened via Live Server (port 5500) or file://, force it to use the Flask backend on port 5000.
let API_BASE = '';
if (window.location.protocol === 'file:' || ((window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost') && window.location.port !== '5000')) {
    API_BASE = 'http://127.0.0.1:5000';
}

// ============ TAB SWITCHING ============
function switchTab(tabName) {
    currentTab = tabName;

    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(el => {
        el.classList.remove('active');
        setTimeout(() => el.style.display = 'none', 10);
    });

    // Show target tab
    const target = document.getElementById(`tab-${tabName}`);
    if (target) {
        setTimeout(() => {
            target.style.display = 'block';
            void target.offsetWidth; // Force reflow
            target.classList.add('active');

            // Trigger stagger animations for current tab
            const staggerItems = target.querySelectorAll('.stagger-item');
            staggerItems.forEach(item => item.classList.remove('active'));
            setTimeout(() => {
                staggerItems.forEach(item => item.classList.add('active'));
            }, 50);
        }, 15);
    }

    // Update nav links
    document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(el => {
        el.classList.remove('active');
        if (el.getAttribute('data-tab') === tabName) {
            el.classList.add('active');
        }
    });

    if (tabName === 'dashboard') loadDashboard();
    if (tabName === 'history') loadHistory();

    if (typeof lucide !== 'undefined') lucide.createIcons();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============ ARCHITECT (GENERATE) LOGIC ============

function selectDomainCard(element) {
    // Remove active from all domain cards
    document.querySelectorAll('.domain-card').forEach(card => card.classList.remove('active'));
    // Add to current
    element.classList.add('active');
    // Update hidden input
    document.getElementById('gen-domain').value = element.getAttribute('data-value');
    showToast(`Domain set to ${element.querySelector('span').textContent}`, 'info');
}

function selectMoodCard(element, mood) {
    // Remove active from all mood cards
    document.querySelectorAll('.mood-card').forEach(card => card.classList.remove('active'));
    // Add to current
    element.classList.add('active');
    // Update hidden input
    document.getElementById('gen-tone-hidden').value = mood;
    showToast(`Mood set to ${mood}`, 'info');
}

// ============ MOBILE MENU ============
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
        menu.style.maxHeight = '0px';
        menu.style.opacity = '0';
        
        // Trigger reflow
        void menu.offsetWidth;
        
        menu.style.transition = 'max-height 0.3s ease-out, opacity 0.3s ease-out';
        menu.style.maxHeight = '300px';
        menu.style.opacity = '1';
    } else {
        menu.style.maxHeight = '0px';
        menu.style.opacity = '0';
        setTimeout(() => {
            menu.classList.add('hidden');
        }, 300);
    }
}

// ============ ANALYZE ============
const analyzeInput = document.getElementById('analyze-input');
const charCount = document.getElementById('char-count');

if (analyzeInput) {
    analyzeInput.addEventListener('input', () => {
        charCount.textContent = `${analyzeInput.value.length} characters`;
    });
}

async function analyzeText() {
    const input = document.getElementById('analyze-input');
    const text = input.value.trim();
    
    if (!text) {
        showToast('Please enter some feedback first.', 'error');
        input.classList.add('ring-2', 'ring-red-500/50');
        setTimeout(() => input.classList.remove('ring-2', 'ring-red-500/50'), 2000);
        return;
    }

    const btn = document.getElementById('analyze-btn');
    const loading = document.getElementById('analyze-loading');
    const results = document.getElementById('analyze-results');

    // UI State: Loading
    btn.disabled = true;
    btn.classList.add('opacity-50', 'cursor-not-allowed');
    loading.classList.remove('hidden');
    loading.classList.add('flex');
    results.classList.add('hidden');
    results.classList.remove('active');
    input.parentElement.classList.add('shimmer-bg');

    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (data.success) {
            displayAnalysisResults(data);
            showToast('Analysis complete!', 'success');
            
            // Animation for results
            loading.classList.add('hidden');
            loading.classList.remove('flex');
            results.classList.remove('hidden');
            setTimeout(() => results.classList.add('active'), 10);
        } else {
            showToast(data.error || 'Analysis failed.', 'error');
        }
    } catch (err) {
        console.error('Analysis error:', err);
        showToast('Failed to connect to server.', 'error');
    } finally {
        btn.disabled = false;
        btn.classList.remove('opacity-50', 'cursor-not-allowed');
        input.parentElement.classList.remove('shimmer-bg');
        if (loading.classList.contains('flex')) {
            loading.classList.add('hidden');
            loading.classList.remove('flex');
        }
    }
}

function displayAnalysisResults(data) {
    const results = document.getElementById('analyze-results');
    results.classList.remove('hidden');
    // small timeout to allow display:block before adding active for animation
    setTimeout(() => {
        results.classList.add('active', 'block');
    }, 10);

    // Sentiment
    const sentiment = data.sentiment;
    const sentimentEl = document.getElementById('result-sentiment');
    sentimentEl.textContent = sentiment.label;
    
    if (sentiment.label === 'Positive') sentimentEl.className = 'text-2xl font-bold bg-gradient-to-r from-emerald-400 to-green-400 bg-clip-text text-transparent drop-shadow-[0_0_10px_rgba(52,211,153,0.3)]';
    else if (sentiment.label === 'Negative') sentimentEl.className = 'text-2xl font-bold bg-gradient-to-r from-red-400 to-rose-400 bg-clip-text text-transparent drop-shadow-[0_0_10px_rgba(248,113,113,0.3)]';
    else sentimentEl.className = 'text-2xl font-bold bg-gradient-to-r from-amber-400 to-yellow-400 bg-clip-text text-transparent drop-shadow-[0_0_10px_rgba(251,191,36,0.3)]';

    document.getElementById('result-score').textContent = sentiment.score.toFixed(4);

    // Confidence bars
    const posPercent = Math.round(sentiment.details.pos * 100);
    const neuPercent = Math.round(sentiment.details.neu * 100);
    const negPercent = Math.round(sentiment.details.neg * 100);

    document.getElementById('result-pos').textContent = `Pos: ${posPercent}%`;
    document.getElementById('result-neu').textContent = `Neu: ${neuPercent}%`;
    document.getElementById('result-neg').textContent = `Neg: ${negPercent}%`;

    const fillEl = document.getElementById('confidence-fill');
    const absScore = Math.abs(sentiment.score);
    // Reset to 0 then animate
    fillEl.style.width = '0%';
    
    setTimeout(() => {
        fillEl.style.width = `${Math.round(absScore * 100)}%`;
        if (sentiment.label === 'Positive') {
            fillEl.className = 'h-full rounded-full transition-all duration-1000 ease-out bg-gradient-to-r from-emerald-500 to-green-400 shadow-[0_0_15px_rgba(52,211,153,0.6)]';
        } else if (sentiment.label === 'Negative') {
            fillEl.className = 'h-full rounded-full transition-all duration-1000 ease-out bg-gradient-to-r from-red-500 to-rose-400 shadow-[0_0_15px_rgba(248,113,113,0.6)]';
        } else {
            fillEl.className = 'h-full rounded-full transition-all duration-1000 ease-out bg-gradient-to-r from-amber-500 to-yellow-400 shadow-[0_0_15px_rgba(251,191,36,0.6)]';
        }
    }, 100);

    // AI Detection
    const ai = data.ai_detection;
    const aiClassEl = document.getElementById('result-ai-class');
    aiClassEl.textContent = ai.classification;
    if (ai.classification === 'Likely AI') {
        aiClassEl.className = 'text-xl font-bold text-red-400 drop-shadow-[0_0_8px_rgba(248,113,113,0.4)]';
    } else if (ai.classification === 'Possibly AI') {
        aiClassEl.className = 'text-xl font-bold text-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.4)]';
    } else {
        aiClassEl.className = 'text-xl font-bold text-emerald-400 drop-shadow-[0_0_8px_rgba(52,211,153,0.4)]';
    }

    document.getElementById('result-ai-score').textContent = `${(ai.confidence * 100).toFixed(1)}%`;
    document.getElementById('result-ai-explanation').textContent = ai.explanation;

    // AI Features
    const featuresEl = document.getElementById('ai-features');
    featuresEl.innerHTML = '';
    if (ai.features) {
        const featureNames = {
            vocabulary_diversity: 'Vocabulary',
            sentence_consistency: 'Consistency',
            repetition: 'Repetition',
            formality: 'Formality',
            punctuation_regularity: 'Punctuation'
        };
        for (const [key, value] of Object.entries(ai.features)) {
            const pct = Math.round(value * 100);
            featuresEl.innerHTML += `
                <div class="feature-meter">
                    <div class="feature-meter-label">${featureNames[key] || key}</div>
                    <div class="feature-meter-bar">
                        <div class="feature-meter-fill" style="width: 0%" data-target="${pct}%"></div>
                    </div>
                    <div class="feature-meter-value">${pct}%</div>
                </div>
            `;
        }
        
        // Animate feature bars
        setTimeout(() => {
            document.querySelectorAll('.feature-meter-fill').forEach(bar => {
                bar.style.width = bar.getAttribute('data-target');
            });
        }, 150);
    }

    // Keywords
    const keywordsEl = document.getElementById('result-keywords');
    keywordsEl.innerHTML = '';
    if (data.keywords && data.keywords.length > 0) {
        data.keywords.forEach(kw => {
            keywordsEl.innerHTML += `<span class="keyword-tag">${kw}</span>`;
        });
    } else {
        keywordsEl.innerHTML = '<span class="text-sm text-gray-500">No significant keywords found.</span>';
    }

    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function clearAnalysis() {
    analyzeInput.value = '';
    charCount.textContent = '0 characters';
    const results = document.getElementById('analyze-results');
    results.classList.remove('active', 'block');
    // Short delay before hiding completely to allow fade out
    setTimeout(() => {
        results.classList.add('hidden');
    }, 300);
}

// ============ GENERATE ============
async function generateFeedback() {
    const domain = document.getElementById('gen-domain').value;
    const tone = document.getElementById('gen-tone-hidden').value;

    const btn = document.getElementById('generate-btn');
    const loading = document.getElementById('gen-loading');
    const output = document.getElementById('gen-output');
    const outputText = document.getElementById('gen-output-text');
    const actions = document.getElementById('gen-actions');
    const status = document.getElementById('stream-status');

    // Reset UI
    outputText.textContent = '';
    actions.classList.add('hidden');
    output.classList.add('hidden');
    loading.classList.remove('hidden');
    status.textContent = 'CONNECTING...';
    status.classList.replace('text-brand-400', 'text-amber-400');

    try {
        const response = await fetch(`${API_BASE}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ domain, tone })
        });

        const data = await response.json();
        
        loading.classList.add('hidden');
        status.textContent = 'STREAMING_FINAL';
        status.classList.replace('text-amber-400', 'text-emerald-400');

        if (data.success) {
            generatedText = data.result.feedback;
            typeWriter(generatedText, 'gen-output-text');
            setTimeout(() => {
                actions.classList.remove('hidden');
            }, (generatedText.length * 20) + 200); // Wait for typewriter to finish mostly
            showToast('Feedback synthesized!', 'success');
        } else {
            showToast(data.error || 'Generation failed', 'error');
            output.classList.remove('hidden');
            status.textContent = 'ERROR';
            status.classList.replace('text-emerald-400', 'text-red-400');
        }
    } catch (err) {
        console.error(err);
        loading.classList.add('hidden');
        output.classList.remove('hidden');
        showToast('System connection error', 'error');
        status.textContent = 'DISCONNECTED';
        status.classList.replace('text-amber-400', 'text-red-400');
    } finally {
        btn.disabled = false;
        btn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

function typeWriter(text, elementId, i = 0) {
    const element = document.getElementById(elementId);
    if (!element) return;

    if (i < text.length) {
        element.innerHTML += text.charAt(i);
        setTimeout(() => typeWriter(text, elementId, i + 1), 10); // Adjust typing speed here
    }
}

function copyGenerated() {
    if (!generatedText) return;

    // Use modern clipboard API if available and securely contexted
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(generatedText).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Clipboard error:', err);
            fallbackCopyTextToClipboard(generatedText);
        });
    } else {
        // Fallback for non-https live servers
        fallbackCopyTextToClipboard(generatedText);
    }
}

function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    
    // Move out of view
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showToast('Copied to clipboard!', 'success');
        } else {
            showToast('Failed to copy. Try highlighting and copying manually.', 'error');
        }
    } catch (err) {
        console.error('Fallback copy error:', err);
        showToast('Failed to copy.', 'error');
    }
    
    document.body.removeChild(textArea);
}

function analyzeGenerated() {
    if (generatedText) {
        // First fill the input
        const input = document.getElementById('analyze-input');
        if (input) {
            input.value = generatedText;
            charCount.textContent = `${generatedText.length} characters`;
        }
        
        // Then switch tab
        switchTab('analyze');
        
        // Scroll to input to show it worked
        setTimeout(() => {
            const el = document.getElementById('analyze-input');
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 150);
    } else {
        showToast('No feedback generated yet.', 'info');
    }
}

// ============ CUSTOM SELECT DROPDOWN ============
function toggleCustomSelect(containerId) {
    const container = document.getElementById(containerId);
    const options = container.querySelector('.custom-select-options');
    const arrow = container.querySelector('.dropdown-arrow');
    
    // Close any other open selects first
    document.querySelectorAll('.custom-select-options.active').forEach(openOptions => {
        if (openOptions !== options) {
            openOptions.classList.remove('active');
            openOptions.previousElementSibling.querySelector('.dropdown-arrow')?.classList.remove('rotate-180');
        }
    });

    options.classList.toggle('active');
    arrow?.classList.toggle('rotate-180');
}

function selectOption(containerId, optionEl) {
    const container = document.getElementById(containerId);
    const value = optionEl.dataset.value;
    const text = optionEl.textContent;
    const hiddenInput = container.querySelector('input[type="hidden"]');
    const triggerText = container.querySelector('#selected-domain-text');
    
    // Update visuals
    container.querySelectorAll('.custom-select-option').forEach(opt => opt.classList.remove('selected'));
    optionEl.classList.add('selected');
    triggerText.textContent = text;
    
    // Update value
    hiddenInput.value = value;
    
    // Close
    toggleCustomSelect(containerId);
}

// Global click listener for dropdowns
document.addEventListener('click', (e) => {
    if (!e.target.closest('.custom-select-container')) {
        document.querySelectorAll('.custom-select-options.active').forEach(options => {
            options.classList.remove('active');
            options.previousElementSibling.querySelector('.dropdown-arrow')?.classList.remove('rotate-180');
        });
    }
});

// ============ DASHBOARD ============
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();

        if (!data.success) return;

        const summary = data.summary;

        // Animate numbers
        animateValue('stat-total', 0, summary.total || 0, 1000);
        
        document.getElementById('stat-positive').textContent = `${summary.positive_pct || 0}%`;
        document.getElementById('stat-negative').textContent = `${summary.negative_pct || 0}%`;
        document.getElementById('stat-avg').textContent = (summary.avg_score || 0).toFixed(2);

        // Styling based on score
        const avgEl = document.getElementById('stat-avg');
        if (summary.avg_score > 0.2) avgEl.className = 'text-3xl font-extrabold text-emerald-400 drop-shadow-[0_0_8px_rgba(52,211,153,0.5)]';
        else if (summary.avg_score < -0.2) avgEl.className = 'text-3xl font-extrabold text-red-400 drop-shadow-[0_0_8px_rgba(248,113,113,0.5)]';
        else avgEl.className = 'text-3xl font-extrabold text-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.5)]';

        // Update neon accents on stat cards
        if (summary.positive_pct > 50) {
           document.getElementById('card-pos').style.boxShadow = '0 0 20px -5px rgba(52, 211, 153, 0.2)';
           document.getElementById('card-pos').style.borderColor = 'rgba(52, 211, 153, 0.3)';
        } else {
           // Reset styles
           document.getElementById('card-pos').style = '';
        }
        
        if (summary.negative_pct > 40) {
           document.getElementById('card-neg').style.boxShadow = '0 0 20px -5px rgba(248, 113, 113, 0.2)';
           document.getElementById('card-neg').style.borderColor = 'rgba(248, 113, 113, 0.3)';
        } else {
           document.getElementById('card-neg').style = '';
        }

        // Pie chart
        renderPieChart(data.sentiment_distribution);

        // Bar chart
        renderBarChart(data.trend_data);

        // Insights
        const insightsList = document.getElementById('insights-list');
        if (summary.insights && summary.insights.length > 0) {
            insightsList.innerHTML = summary.insights.map((i, idx) =>
                `<div class="insight-item" style="animation-delay: ${idx * 0.1}s">
                    <div class="insight-icon bg-blue-500/20 text-blue-400 p-2 rounded-lg flex-shrink-0">
                        <i data-lucide="zap" class="w-4 h-4"></i>
                    </div>
                    <span class="text-gray-300">${i}</span>
                </div>`
            ).join('');
        } else {
            insightsList.innerHTML = '<p class="text-sm text-gray-500 italic">No insights available.</p>';
        }

        // Alerts
        const alertsList = document.getElementById('alerts-list');
        if (summary.alerts && summary.alerts.length > 0) {
            alertsList.innerHTML = summary.alerts.map((a, idx) =>
                `<div class="alert-${a.level}" style="animation-delay: ${idx * 0.1}s">
                    <div class="flex items-start gap-3">
                        ${a.level === 'critical' 
                            ? '<i data-lucide="alert-octagon" class="w-5 h-5 text-red-500 mt-0.5 animate-pulse"></i>' 
                            : '<i data-lucide="alert-triangle" class="w-5 h-5 text-amber-500 mt-0.5"></i>'
                        }
                        <p class="text-sm font-medium ${a.level === 'critical' ? 'text-red-200' : 'text-amber-200'}">${a.message.replace(/^[🔴🟡\?]+\s*(Critical|Warning):\s*/, '')}</p>
                    </div>
                </div>`
            ).join('');
        } else {
            alertsList.innerHTML = `
                <div class="glass-card rounded-xl p-4 flex items-center gap-3 border-emerald-500/30 bg-emerald-500/5">
                    <div class="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                        <i data-lucide="check" class="w-4 h-4"></i>
                    </div>
                    <span class="text-sm font-medium text-emerald-300">No alerts — everything looks good!</span>
                </div>
            `;
        }

        // Keywords
        const kw = document.getElementById('dashboard-keywords');
        if (summary.top_keywords && summary.top_keywords.length > 0) {
            kw.innerHTML = summary.top_keywords.map((k, idx) =>
                `<span class="keyword-tag" style="animation-delay: ${idx * 0.05}s">${k}</span>`
            ).join('');
        } else {
            kw.innerHTML = '<p class="text-sm text-gray-500 italic">No keywords yet.</p>';
        }

        // Re-init lucide icons for new content
        if (typeof lucide !== 'undefined') lucide.createIcons();

    } catch (err) {
        console.error('Dashboard load error:', err);
    }
}

// Simple number animation
function animateValue(id, start, end, duration) {
    if (start === end) return;
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        // Easing out cubic
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        obj.innerHTML = Math.floor(easeProgress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Chart defaults for dark theme
Chart.defaults.color = '#9ca3af';
Chart.defaults.font.family = 'Inter, sans-serif';

function renderPieChart(distData) {
    const ctx = document.getElementById('sentimentPieChart');
    if (!ctx) return;

    if (pieChart) pieChart.destroy();

    const hasData = distData && distData.data && distData.data.some(v => v > 0);

    pieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: hasData ? distData.labels : ['No Data'],
            datasets: [{
                data: hasData ? distData.data : [1],
                backgroundColor: hasData ? ['#10B981', '#EF4444', '#F59E0B'] : ['#374151'],
                borderWidth: 2,
                borderColor: '#111827', // Match background
                hoverOffset: 10,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyleWidth: 10,
                        font: { size: 13, weight: '500' },
                        color: '#d1d5db'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.9)',
                    titleColor: '#f3f4f6',
                    bodyColor: '#d1d5db',
                    borderColor: 'rgba(55, 65, 81, 0.5)',
                    borderWidth: 1,
                    padding: 12,
                    boxPadding: 6,
                    cornerRadius: 8,
                    displayColors: true
                }
            }
        }
    });
}

function renderBarChart(trendData) {
    const ctx = document.getElementById('trendBarChart');
    if (!ctx) return;

    if (barChart) barChart.destroy();

    const hasData = trendData && trendData.labels && trendData.labels.length > 0;

    // Create gradients
    const createGrad = (color1, color2) => {
        const grd = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
        grd.addColorStop(0, color1);
        grd.addColorStop(1, color2);
        return grd;
    };

    barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hasData ? trendData.labels : ['No data yet'],
            datasets: hasData ? [
                {
                    label: 'Positive',
                    data: trendData.positive,
                    backgroundColor: createGrad('rgba(16, 185, 129, 0.8)', 'rgba(5, 150, 105, 0.5)'),
                    borderColor: '#10B981',
                    borderWidth: 1,
                    borderRadius: 6,
                    barPercentage: 0.6
                },
                {
                    label: 'Negative',
                    data: trendData.negative,
                    backgroundColor: createGrad('rgba(239, 68, 68, 0.8)', 'rgba(220, 38, 38, 0.5)'),
                    borderColor: '#EF4444',
                    borderWidth: 1,
                    borderRadius: 6,
                    barPercentage: 0.6
                },
                {
                    label: 'Neutral',
                    data: trendData.neutral,
                    backgroundColor: createGrad('rgba(245, 158, 11, 0.8)', 'rgba(217, 119, 6, 0.5)'),
                    borderColor: '#F59E0B',
                    borderWidth: 1,
                    borderRadius: 6,
                    barPercentage: 0.6
                }
            ] : [{
                label: 'No data',
                data: [0],
                backgroundColor: '#374151',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 12 }, color: '#9ca3af' }
                },
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(55, 65, 81, 0.3)', drawBorder: false },
                    ticks: {
                        stepSize: 1,
                        font: { size: 12 },
                        color: '#9ca3af',
                        padding: 10
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyleWidth: 10,
                        font: { size: 13, weight: '500' },
                        color: '#d1d5db'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.9)',
                    titleColor: '#f3f4f6',
                    bodyColor: '#d1d5db',
                    borderColor: 'rgba(55, 65, 81, 0.5)',
                    borderWidth: 1,
                    padding: 12,
                    boxPadding: 6,
                    cornerRadius: 8
                }
            }
        }
    });
}

// ============ HISTORY ============
async function loadHistory() {
    const list = document.getElementById('history-list');
    const loading = document.getElementById('history-loading');

    list.classList.add('hidden');
    
    loading.classList.remove('hidden');
    loading.classList.add('flex');

    try {
        const response = await fetch(`${API_BASE}/history`);
        const data = await response.json();

        loading.classList.remove('flex');
        loading.classList.add('hidden');
        list.classList.remove('hidden');
        // Triger reflow
        void list.offsetWidth;

        if (!data.success || !data.feedbacks || data.feedbacks.length === 0) {
            list.innerHTML = `
                <div class="glass-card text-center py-16 flex flex-col items-center animate-fade-in-up">
                    <div class="w-20 h-20 bg-gray-800/50 rounded-full flex items-center justify-center mb-5 border border-gray-700/50 shadow-inner">
                        <i data-lucide="inbox" class="w-10 h-10 text-gray-500"></i>
                    </div>
                    <p class="text-xl font-medium text-gray-300 mb-2">No feedback history yet</p>
                    <p class="text-gray-500">Go to the Analyze tab to evaluate your first piece of feedback.</p>
                    <button onclick="switchTab('analyze')" class="mt-6 btn-primary">Start Analyzing</button>
                </div>
            `;
        } else {
            list.innerHTML = data.feedbacks.map((f, i) => {
                const isPos = f.sentiment === 'Positive';
                const isNeg = f.sentiment === 'Negative';
                const sentClass = isPos ? 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10' :
                                  isNeg ? 'text-red-400 border-red-500/30 bg-red-500/10' :
                                  'text-amber-400 border-amber-500/30 bg-amber-500/10';
                                  
                const scoreColor = isPos ? 'text-emerald-500' : isNeg ? 'text-red-500' : 'text-amber-500';                  
                
                const isLikelyAI = f.ai_detection === 'Likely AI';
                const isPossAI = f.ai_detection === 'Possibly AI';
                const aiClass = isLikelyAI ? 'text-red-400 border-red-500/30 bg-red-500/10' :
                                isPossAI ? 'text-amber-400 border-amber-500/30 bg-amber-500/10' :
                                'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
                                
                const timeStr = f.timestamp ? new Date(f.timestamp).toLocaleString([], {
                    month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit'
                }) : 'Unknown';
                
                const truncText = f.text.length > 250 ? f.text.substring(0, 250) + '...' : f.text;

                return `
                    <div class="history-entry" style="animation-delay: ${i * 0.05}s">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                            <div class="flex items-center gap-2 flex-wrap">
                                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${sentClass}">
                                    ${isPos ? '<i data-lucide="trending-up" class="w-3.5 h-3.5"></i>' : 
                                      isNeg ? '<i data-lucide="trending-down" class="w-3.5 h-3.5"></i>' : 
                                      '<i data-lucide="minus" class="w-3.5 h-3.5"></i>'}
                                    ${f.sentiment} 
                                    <span class="opacity-70 font-mono ml-1">${f.score >= 0 ? '+' : ''}${f.score.toFixed(2)}</span>
                                </span>
                                
                                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${aiClass}">
                                    ${isLikelyAI ? '<i data-lucide="bot" class="w-3.5 h-3.5"></i>' : 
                                      isPossAI ? '<i data-lucide="search" class="w-3.5 h-3.5"></i>' : 
                                      '<i data-lucide="user" class="w-3.5 h-3.5"></i>'}
                                    ${f.ai_detection}
                                </span>
                            </div>
                            <div class="flex items-center gap-1.5 text-xs text-gray-500 whitespace-nowrap bg-gray-800/50 px-3 py-1.5 rounded-lg">
                                <i data-lucide="clock" class="w-3.5 h-3.5"></i>
                                ${timeStr}
                            </div>
                        </div>
                        <p class="text-sm text-gray-300 leading-relaxed border-l-2 ${isPos ? 'border-emerald-500/30' : isNeg ? 'border-red-500/30' : 'border-amber-500/30'} pl-4 py-1">${truncText}</p>
                    </div>
                `;
            }).join('');
        }

    } catch (err) {
        console.error('History error:', err);
        loading.classList.remove('flex');
        loading.classList.add('hidden');
        list.classList.remove('hidden');
        list.innerHTML = `
            <div class="glass-card text-center py-12 border-red-500/20 bg-red-500/5">
                <i data-lucide="alert-circle" class="w-12 h-12 text-red-400 mx-auto mb-3"></i>
                <p class="text-red-400 font-medium text-lg">Failed to load history.</p>
                <p class="text-red-500/70 text-sm mt-1">Make sure the Flask server is running.</p>
                <button onclick="loadHistory()" class="mt-4 px-4 py-2 bg-gray-800 rounded-lg text-sm text-gray-300 hover:text-white transition-colors">Try Again</button>
            </div>
        `;
    }

    if (typeof lucide !== 'undefined') lucide.createIcons();
}

async function clearHistory() {
    if (!confirm('Are you sure you want to clear all feedback data? This action cannot be undone.')) return;

    try {
        const response = await fetch(`${API_BASE}/clear`, { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            showToast('All feedback data cleared.', 'success');
            loadHistory();
        }
    } catch (err) {
        showToast('Failed to clear data.', 'error');
    }
}

// ============ TOAST NOTIFICATION ============
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const msgEl = document.getElementById('toast-message');
    const iconEl = document.getElementById('toast-icon');
    
    msgEl.textContent = message;
    
    // Set icon and colors based on type
    if (type === 'success') {
        iconEl.innerHTML = '<i data-lucide="check-circle" class="w-5 h-5 text-emerald-400"></i>';
        toast.className = 'fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 pointer-events-none transition-all duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]';
        toast.querySelector('.toast-inner').className = 'toast-inner flex items-center gap-3 px-5 py-3.5 bg-gray-800/90 backdrop-blur-md rounded-2xl shadow-[0_10px_40px_-10px_rgba(16,185,129,0.3)] border border-gray-700/50';
    } else if (type === 'info') {
        iconEl.innerHTML = '<i data-lucide="info" class="w-5 h-5 text-brand-400"></i>';
        toast.className = 'fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 pointer-events-none transition-all duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]';
        toast.querySelector('.toast-inner').className = 'toast-inner flex items-center gap-3 px-5 py-3.5 bg-gray-800/90 backdrop-blur-md rounded-2xl shadow-[0_10px_40px_-10px_rgba(14,165,233,0.3)] border border-brand-500/30';
    } else {
        iconEl.innerHTML = '<i data-lucide="alert-circle" class="w-5 h-5 text-red-400"></i>';
        toast.className = 'fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 pointer-events-none transition-all duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]';
        toast.querySelector('.toast-inner').className = 'toast-inner flex items-center gap-3 px-5 py-3.5 bg-gray-800/90 backdrop-blur-md rounded-2xl shadow-[0_10px_40px_-10px_rgba(239,68,68,0.3)] border border-red-500/30';
    }
    
    if (typeof lucide !== 'undefined') lucide.createIcons();

    // Force reflow
    void toast.offsetWidth;

    // Show
    toast.classList.remove('translate-y-20', 'opacity-0', 'pointer-events-none');
    toast.classList.add('translate-y-0', 'opacity-100');

    // Hide after timeout
    setTimeout(() => {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-20', 'opacity-0', 'pointer-events-none');
    }, 4000);
}

// ============ NAVBAR SCROLL EFFECT ============
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;
    
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > 20) {
        navbar.classList.add('bg-gray-900/80', 'backdrop-blur-xl', 'border-gray-800', 'shadow-[0_4px_30px_rgba(0,0,0,0.1)]');
        navbar.classList.remove('bg-transparent', 'border-transparent');
    } else {
        navbar.classList.remove('bg-gray-900/80', 'backdrop-blur-xl', 'border-gray-800', 'shadow-[0_4px_30px_rgba(0,0,0,0.1)]');
        navbar.classList.add('bg-transparent', 'border-transparent');
    }
    lastScroll = scrollTop;
});

// ============ INIT ============
document.addEventListener('DOMContentLoaded', () => {
    if (typeof lucide !== 'undefined') lucide.createIcons();
    
    // Create matrix/stars background effect on body
    createBackgroundEffect();
    
    // Trigger initial tab to run animations
    switchTab(currentTab);
    
    // Trigger scroll event to set initial navbar state
    window.dispatchEvent(new Event('scroll'));
});

function createBackgroundEffect() {
    const bg = document.createElement('div');
    bg.className = 'fixed inset-0 z-[-1] overflow-hidden pointer-events-none';
    bg.innerHTML = `
        <div class="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-blue-600/10 blur-[120px]"></div>
        <div class="absolute bottom-[-20%] right-[-10%] w-[60%] h-[60%] rounded-full bg-indigo-600/10 blur-[150px]"></div>
        <div class="absolute top-[40%] right-[20%] w-[30%] h-[40%] rounded-full bg-emerald-600/5 blur-[100px]"></div>
    `;
    document.body.prepend(bg);
}
