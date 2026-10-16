/**
 * MediAI Pro — Laboratory Test Analyzer Controller
 * Architected by Shashank Dixit
 */

const LabAnalyzer = {
    init() {
        this.setupPresets();
        this.setupForm();
    },

    setupPresets() {
        const presetNormal = document.getElementById('load-normal-lab-preset');
        const presetDiabetic = document.getElementById('load-diabetic-lab-preset');
        const presetRenal = document.getElementById('load-renal-lab-preset');
        const clearBtn = document.getElementById('clear-lab-form-btn');

        if (presetNormal) {
            presetNormal.addEventListener('click', () => {
                this.fillValues({
                    'lab-hemoglobin': '14.8',
                    'lab-wbc': '6.4',
                    'lab-platelets': '240',
                    'lab-fasting_glucose': '88',
                    'lab-hba1c': '5.2',
                    'lab-creatinine': '0.9',
                    'lab-egfr': '105',
                    'lab-total_cholesterol': '170',
                    'lab-ldl': '85',
                    'lab-hdl': '55',
                    'lab-triglycerides': '110',
                    'lab-alt': '22',
                    'lab-ast': '24',
                    'lab-tsh': '1.8',
                    'lab-crp': '0.8'
                });
                App.showToast('Loaded normal laboratory panel preset', 'success');
            });
        }

        if (presetDiabetic) {
            presetDiabetic.addEventListener('click', () => {
                this.fillValues({
                    'lab-hemoglobin': '13.2',
                    'lab-wbc': '8.2',
                    'lab-platelets': '290',
                    'lab-fasting_glucose': '185',
                    'lab-hba1c': '8.6',
                    'lab-creatinine': '1.3',
                    'lab-egfr': '68',
                    'lab-total_cholesterol': '245',
                    'lab-ldl': '158',
                    'lab-hdl': '38',
                    'lab-triglycerides': '280',
                    'lab-alt': '45',
                    'lab-ast': '38',
                    'lab-tsh': '2.4',
                    'lab-crp': '4.5'
                });
                App.showToast('Loaded Diabetic & Dyslipidemia panel preset', 'warning');
            });
        }

        if (presetRenal) {
            presetRenal.addEventListener('click', () => {
                this.fillValues({
                    'lab-hemoglobin': '9.8',
                    'lab-wbc': '14.8',
                    'lab-platelets': '160',
                    'lab-fasting_glucose': '110',
                    'lab-hba1c': '6.1',
                    'lab-creatinine': '3.4',
                    'lab-egfr': '18',
                    'lab-total_cholesterol': '190',
                    'lab-ldl': '110',
                    'lab-hdl': '42',
                    'lab-triglycerides': '165',
                    'lab-alt': '35',
                    'lab-ast': '40',
                    'lab-tsh': '3.1',
                    'lab-crp': '28.0'
                });
                App.showToast('Loaded Renal & Inflammatory panel preset', 'danger');
            });
        }

        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                document.getElementById('lab-analysis-form')?.reset();
                document.getElementById('lab-results-container')?.classList.add('hidden');
                App.showToast('Lab form cleared', 'info');
            });
        }
    },

    fillValues(mapping) {
        for (const [id, val] of Object.entries(mapping)) {
            const input = document.getElementById(id);
            if (input) input.value = val;
        }
    },

    setupForm() {
        const form = document.getElementById('lab-analysis-form');
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.analyzeLabs();
            });
        }
    },

    async analyzeLabs() {
        const btn = document.getElementById('run-lab-analysis-btn');
        const origText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Biomarkers...`;

        try {
            const values = {};
            const keys = [
                'hemoglobin', 'wbc', 'platelets', 'fasting_glucose', 'hba1c',
                'creatinine', 'egfr', 'total_cholesterol', 'ldl', 'hdl',
                'triglycerides', 'alt', 'ast', 'tsh', 'crp'
            ];

            keys.forEach(k => {
                const el = document.getElementById(`lab-${k}`);
                if (el && el.value.trim() !== '') {
                    values[k] = parseFloat(el.value.trim());
                }
            });

            if (Object.keys(values).length === 0) {
                App.showToast('Please enter at least one laboratory value to analyze.', 'warning');
                return;
            }

            const res = await fetch('/api/analyze-labs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ values })
            });

            if (!res.ok) throw new Error(`HTTP error ${res.status}`);

            const json = await res.json();
            if (json.success && json.report) {
                App.latestLabData = json.report;
                this.renderLabResults(json.report);
                App.showToast('Lab biomarker evaluation complete!', 'success');
            }
        } catch (err) {
            console.error("Lab evaluation error:", err);
            App.showToast(`Evaluation failed: ${err.message}`, 'danger');
        } finally {
            btn.disabled = false;
            btn.innerHTML = origText;
        }
    },

    renderLabResults(report) {
        const container = document.getElementById('lab-results-container');
        if (!container) return;

        container.classList.remove('hidden');

        const badgeClasses = {
            red: 'bg-rose-50 dark:bg-rose-950/40 border-rose-300 dark:border-rose-800 text-rose-800 dark:text-rose-200',
            amber: 'bg-amber-50 dark:bg-amber-950/40 border-amber-300 dark:border-amber-800 text-amber-800 dark:text-amber-200',
            green: 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200'
        };

        const pillClasses = {
            red: 'bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300 border-rose-200',
            amber: 'bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300 border-amber-200',
            green: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200'
        };

        container.innerHTML = `
            <!-- Top Summary Card -->
            <div class="p-6 rounded-2xl border ${badgeClasses[report.badge_color] || badgeClasses.green} mb-6 shadow-sm">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-3">
                    <div>
                        <div class="text-xs uppercase font-bold tracking-wider">Overall Laboratory Finding</div>
                        <h3 class="text-2xl font-black">${report.overall_severity}</h3>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="px-3 py-1 bg-white/80 dark:bg-slate-800/80 rounded-xl text-xs font-bold shadow-sm">
                            ${report.total_analyzed} Tests Analyzed
                        </span>
                        ${report.abnormal_count > 0 ? `
                        <span class="px-3 py-1 bg-amber-500 text-white rounded-xl text-xs font-bold shadow-sm">
                            ${report.abnormal_count} Deviating
                        </span>
                        ` : ''}
                        ${report.critical_count > 0 ? `
                        <span class="px-3 py-1 bg-rose-600 text-white rounded-xl text-xs font-bold shadow-sm animate-pulse">
                            ${report.critical_count} Critical
                        </span>
                        ` : ''}
                    </div>
                </div>
                <p class="text-sm leading-relaxed">${report.advice}</p>
            </div>

            <!-- Individual Biomarker Cards Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                ${report.tests.map(t => `
                    <div class="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm hover:shadow-md transition">
                        <div class="flex justify-between items-start mb-2">
                            <span class="text-xs font-bold text-slate-700 dark:text-slate-300">${t.name}</span>
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${pillClasses[t.color] || pillClasses.green}">
                                ${t.status}
                            </span>
                        </div>
                        <div class="flex items-baseline gap-1 my-1">
                            <span class="text-2xl font-black text-slate-900 dark:text-white">${t.value}</span>
                            <span class="text-xs text-slate-500">${t.unit}</span>
                        </div>
                        <div class="text-[11px] text-slate-400 mb-2">Reference: ${t.reference_low} - ${t.reference_high} ${t.unit}</div>

                        <!-- Spectrum visual meter bar -->
                        <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full relative overflow-hidden mb-2">
                            <div class="absolute left-0 top-0 h-full w-full bg-gradient-to-r from-blue-300 via-emerald-400 to-rose-400 opacity-60"></div>
                            <div class="absolute top-0 bottom-0 w-1 bg-slate-900 dark:bg-white rounded-full shadow" style="left: ${t.bar_percentage}%"></div>
                        </div>

                        <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-tight">${t.interpretation}</p>
                    </div>
                `).join('')}
            </div>

            <!-- Action Bar -->
            <div class="p-4 bg-slate-50 dark:bg-slate-800/40 rounded-2xl border border-slate-200 dark:border-slate-700/60 flex justify-between items-center">
                <span class="text-xs text-slate-500">
                    <i class="fa-solid fa-circle-info text-sky-500 mr-1"></i> Reference intervals based on adult clinical laboratory standards.
                </span>
                <button onclick="App.switchTab('report-tab')" class="px-4 py-2 bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold rounded-xl shadow transition">
                    View in Full Report
                </button>
            </div>
        `;

        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
};

window.addEventListener('DOMContentLoaded', () => {
    LabAnalyzer.init();
});
