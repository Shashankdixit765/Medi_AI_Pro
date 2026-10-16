/**
 * MediAI Pro — Main Client App Controller
 * Architected by Shashank Dixit
 */

const App = {
    currentTab: 'symptom-tab',
    darkMode: false,
    apiKey: localStorage.getItem('mediai_gemini_key') || '',
    latestDiagnosisData: null,
    latestLabData: null,

    init() {
        this.setupTheme();
        this.setupNavigation();
        this.setupSettingsModal();
        this.loadHotlines();
        console.log("MediAI Pro initialized. Architected by Shashank Dixit.");
    },

    setupTheme() {
        const savedTheme = localStorage.getItem('mediai_theme');
        if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
            this.darkMode = true;
            this.updateThemeIcon();
        }

        const themeBtn = document.getElementById('theme-toggle-btn');
        if (themeBtn) {
            themeBtn.addEventListener('click', () => {
                this.darkMode = !this.darkMode;
                if (this.darkMode) {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('mediai_theme', 'dark');
                } else {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('mediai_theme', 'light');
                }
                this.updateThemeIcon();
            });
        }
    },

    updateThemeIcon() {
        const icon = document.getElementById('theme-toggle-icon');
        if (icon) {
            if (this.darkMode) {
                icon.className = 'fa-solid fa-sun text-yellow-400';
            } else {
                icon.className = 'fa-solid fa-moon text-slate-600';
            }
        }
    },

    setupNavigation() {
        const navTabs = document.querySelectorAll('.nav-tab');
        navTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                const target = tab.getAttribute('data-tab');
                this.switchTab(target);
            });
        });
    },

    switchTab(tabId) {
        // Update nav buttons
        document.querySelectorAll('.nav-tab').forEach(t => {
            if (t.getAttribute('data-tab') === tabId) {
                t.classList.add('active');
            } else {
                t.classList.remove('active');
            }
        });

        // Hide all tab panes
        document.querySelectorAll('.tab-content-pane').forEach(pane => {
            pane.classList.add('hidden');
        });

        // Show target pane
        const activePane = document.getElementById(tabId);
        if (activePane) {
            activePane.classList.remove('hidden');
            this.currentTab = tabId;
        }

        // If switching to report tab, refresh report view
        if (tabId === 'report-tab') {
            this.renderConsultationReport();
        }

        // Scroll to top smoothly
        window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    setupSettingsModal() {
        const modal = document.getElementById('settings-modal');
        const openBtn = document.getElementById('open-settings-btn');
        const closeBtn = document.getElementById('close-settings-btn');
        const saveBtn = document.getElementById('save-settings-btn');
        const keyInput = document.getElementById('gemini-api-key-input');

        if (keyInput && this.apiKey) {
            keyInput.value = this.apiKey;
        }

        if (openBtn && modal) {
            openBtn.addEventListener('click', () => {
                modal.classList.remove('hidden');
            });
        }

        if (closeBtn && modal) {
            closeBtn.addEventListener('click', () => {
                modal.classList.add('hidden');
            });
        }

        if (saveBtn && keyInput && modal) {
            saveBtn.addEventListener('click', () => {
                this.apiKey = keyInput.value.trim();
                localStorage.setItem('mediai_gemini_key', this.apiKey);
                modal.classList.add('hidden');
                this.showToast('Settings saved successfully!', 'success');
            });
        }
    },

    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        const colors = {
            success: 'bg-emerald-600 text-white',
            danger: 'bg-rose-600 text-white',
            warning: 'bg-amber-500 text-white',
            info: 'bg-sky-600 text-white'
        };

        const icons = {
            success: 'fa-circle-check',
            danger: 'fa-triangle-exclamation',
            warning: 'fa-circle-exclamation',
            info: 'fa-circle-info'
        };

        toast.className = `flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg transform transition-all duration-300 translate-y-2 opacity-0 ${colors[type] || colors.info}`;
        toast.innerHTML = `
            <i class="fa-solid ${icons[type] || icons.info}"></i>
            <span class="text-sm font-medium">${message}</span>
        `;

        container.appendChild(toast);
        requestAnimationFrame(() => {
            toast.classList.remove('translate-y-2', 'opacity-0');
        });

        setTimeout(() => {
            toast.classList.add('opacity-0', 'translate-y-2');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    },

    async loadHotlines() {
        try {
            const res = await fetch('/api/hotlines');
            const data = await res.json();
            const listContainer = document.getElementById('hotlines-list-container');
            if (listContainer && data.hotlines) {
                listContainer.innerHTML = data.hotlines.map(h => `
                    <div class="flex items-center justify-between p-3.5 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200 dark:border-slate-700/60">
                        <div>
                            <div class="font-semibold text-slate-900 dark:text-slate-100">${h.name}</div>
                            <div class="text-xs text-slate-500 dark:text-slate-400">${h.desc}</div>
                        </div>
                        <a href="tel:${h.number}" class="inline-flex items-center gap-2 px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-sm font-bold shadow-sm transition">
                            <i class="fa-solid fa-phone"></i> ${h.number}
                        </a>
                    </div>
                `).join('');
            }
        } catch (e) {
            console.warn("Could not load hotlines:", e);
        }
    },

    renderConsultationReport() {
        const reportContainer = document.getElementById('report-printable-area');
        if (!reportContainer) return;

        const diag = this.latestDiagnosisData;
        const labs = this.latestLabData;

        const now = new Date();
        const formattedDate = now.toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
        });

        if (!diag && !labs) {
            reportContainer.innerHTML = `
                <div class="text-center py-16 px-4">
                    <div class="w-16 h-16 bg-sky-100 dark:bg-sky-950/50 text-sky-600 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
                        <i class="fa-solid fa-notes-medical"></i>
                    </div>
                    <h3 class="text-lg font-bold text-slate-800 dark:text-slate-200">No Assessment Data Yet</h3>
                    <p class="text-sm text-slate-500 dark:text-slate-400 mt-2 max-w-md mx-auto">
                        Please perform an evaluation in the <strong>Symptom Checker & Triage</strong> tab or the <strong>Lab Analyzer</strong> tab to generate your complete clinical summary report.
                    </p>
                    <button onclick="App.switchTab('symptom-tab')" class="mt-6 px-5 py-2.5 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-sm font-semibold shadow-md transition">
                        Go to Symptom Checker
                    </button>
                </div>
            `;
            return;
        }

        const patientName = document.getElementById('patient-name-input')?.value || 'Confidential Patient';
        const patientAge = document.getElementById('patient-age-input')?.value || 'N/A';
        const patientGender = document.getElementById('patient-gender-select')?.value || 'N/A';

        reportContainer.innerHTML = `
            <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-10 shadow-lg print-only-container">
                <!-- Report Header -->
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-6 border-b border-slate-200 dark:border-slate-800 gap-4">
                    <div>
                        <div class="flex items-center gap-3">
                            <span class="p-2.5 bg-sky-600 text-white rounded-xl text-xl">
                                <i class="fa-solid fa-heart-pulse"></i>
                            </span>
                            <div>
                                <h1 class="text-2xl font-black tracking-tight text-slate-900 dark:text-white">MediAI Clinical Consultation Note</h1>
                                <p class="text-xs text-slate-500 dark:text-slate-400">AI Clinical Decision Support & Triage Report</p>
                            </div>
                        </div>
                    </div>
                    <div class="text-right sm:text-right text-xs text-slate-500 dark:text-slate-400">
                        <div><strong>Report Date:</strong> ${formattedDate}</div>
                        <div><strong>System Architect:</strong> Shashank Dixit</div>
                        <div><strong>Status:</strong> Generated & Validated</div>
                    </div>
                </div>

                <!-- Patient & Vitals Row -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6 p-4 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700/60">
                    <div>
                        <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Patient Demographics</h4>
                        <div class="text-sm font-bold text-slate-900 dark:text-white">${patientName}</div>
                        <div class="text-xs text-slate-600 dark:text-slate-300 mt-1">Age: ${patientAge} | Biological Sex: ${patientGender}</div>
                    </div>
                    <div>
                        <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Triage & Vital Signs</h4>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-1 text-xs font-bold rounded-full ${
                                diag?.overall_urgency === 'Emergency' ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300' :
                                diag?.overall_urgency === 'Urgent' ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' :
                                'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                            }">
                                Urgency: ${diag?.overall_urgency || 'Routine'}
                            </span>
                            <span class="text-xs text-slate-600 dark:text-slate-300">
                                NEWS2 Score: ${diag?.vital_assessment?.news2_score ?? '0'}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Primary Clinical Diagnosis -->
                ${diag ? `
                <div class="mb-6">
                    <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-3">
                        <i class="fa-solid fa-stethoscope text-sky-600"></i> Primary Clinical Diagnosis
                    </h3>
                    <div class="p-4 bg-sky-50 dark:bg-sky-950/30 border border-sky-200 dark:border-sky-800/60 rounded-xl">
                        <div class="flex justify-between items-start mb-2">
                            <div>
                                <span class="text-lg font-black text-sky-900 dark:text-sky-100">${diag.primary_diagnosis.name}</span>
                                <span class="ml-2 text-xs font-mono px-2 py-0.5 bg-sky-200 dark:bg-sky-900 text-sky-800 dark:text-sky-200 rounded">ICD-10: ${diag.primary_diagnosis.icd10}</span>
                            </div>
                            <span class="px-3 py-1 bg-sky-600 text-white font-bold text-xs rounded-full">
                                ${diag.primary_diagnosis.probability}% Match
                            </span>
                        </div>
                        <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">${diag.primary_diagnosis.description}</p>
                    </div>
                </div>

                <!-- Differential Diagnoses -->
                ${diag.differential_diagnoses && diag.differential_diagnoses.length > 0 ? `
                <div class="mb-6">
                    <h3 class="text-sm font-bold text-slate-900 dark:text-white mb-2">Differential Diagnoses Considered</h3>
                    <div class="space-y-2">
                        ${diag.differential_diagnoses.map(d => `
                            <div class="flex items-center justify-between p-2.5 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-200 dark:border-slate-700/60 text-xs">
                                <span class="font-medium text-slate-800 dark:text-slate-200">${d.name} (${d.icd10})</span>
                                <span class="font-bold text-slate-600 dark:text-slate-400">${d.probability}% Match</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                ` : ''}

                <!-- Red Flags & Safety Warnings -->
                ${diag.red_flags && diag.red_flags.length > 0 ? `
                <div class="mb-6 p-4 bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/60 rounded-xl">
                    <h4 class="text-xs font-bold text-rose-800 dark:text-rose-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                        <i class="fa-solid fa-triangle-exclamation"></i> Critical Red Flag Alerts & Clinical Warnings
                    </h4>
                    <ul class="list-disc list-inside text-xs text-rose-700 dark:text-rose-400 space-y-1">
                        ${diag.red_flags.map(rf => `<li>${rf}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}

                <!-- Recommended Investigations -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div class="p-4 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700/60">
                        <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Recommended Investigations</h4>
                        <ul class="list-disc list-inside text-xs text-slate-600 dark:text-slate-300 space-y-1">
                            ${diag.recommended_tests.map(t => `<li>${t}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="p-4 bg-slate-50 dark:bg-slate-800/40 rounded-xl border border-slate-200 dark:border-slate-700/60">
                        <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Clinical Management Guidance</h4>
                        <ul class="list-disc list-inside text-xs text-slate-600 dark:text-slate-300 space-y-1">
                            ${diag.clinical_management.map(m => `<li>${m}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                ` : ''}

                <!-- Lab Biomarkers Section if present -->
                ${labs ? `
                <div class="mb-6">
                    <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-3">
                        <i class="fa-solid fa-flask text-teal-600"></i> Laboratory Biomarker Findings
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs border-collapse">
                            <thead>
                                <tr class="border-b border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                                    <th class="p-2">Test Name</th>
                                    <th class="p-2">Observed Value</th>
                                    <th class="p-2">Reference Range</th>
                                    <th class="p-2">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${labs.tests.map(t => `
                                    <tr class="border-b border-slate-100 dark:border-slate-800">
                                        <td class="p-2 font-medium text-slate-800 dark:text-slate-200">${t.name}</td>
                                        <td class="p-2 font-bold text-slate-900 dark:text-white">${t.value} ${t.unit}</td>
                                        <td class="p-2 text-slate-500">${t.reference_low} - ${t.reference_high} ${t.unit}</td>
                                        <td class="p-2">
                                            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${
                                                t.color === 'red' ? 'bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300' :
                                                t.color === 'amber' ? 'bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300' :
                                                'bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300'
                                            }">
                                                ${t.status}
                                            </span>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
                ` : ''}

                <!-- Attestation & Signature -->
                <div class="mt-8 pt-6 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row justify-between items-start sm:items-end gap-6">
                    <div>
                        <div class="text-xs text-slate-400">Software Architecture & Diagnostic Design:</div>
                        <div class="text-sm font-bold text-slate-800 dark:text-slate-200">Shashank Dixit</div>
                        <div class="text-[10px] text-slate-400">MediAI Pro Healthcare Systems</div>
                    </div>
                    <div class="text-left sm:text-right">
                        <div class="border-b border-slate-400 dark:border-slate-600 w-48 mb-1"></div>
                        <div class="text-[10px] text-slate-400">Attending Physician Review & Signature</div>
                    </div>
                </div>

                <!-- Clinical Disclaimer -->
                <div class="mt-6 p-3 bg-slate-100 dark:bg-slate-800/60 rounded-lg text-[10px] text-slate-500 dark:text-slate-400 text-center leading-relaxed">
                    <strong>LEGAL & CLINICAL DISCLAIMER:</strong> This report is produced by MediAI Clinical Decision Support Assistant, designed by Shashank Dixit. It is intended solely for clinical risk stratification and preliminary triage guidance. It does NOT constitute a binding medical diagnosis and cannot substitute for an in-person examination by a licensed medical practitioner.
                </div>
            </div>

            <!-- Print Action Button Bar -->
            <div class="mt-6 flex justify-end gap-3 no-print">
                <button onclick="window.print()" class="px-5 py-2.5 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-sm font-semibold shadow-md transition flex items-center gap-2">
                    <i class="fa-solid fa-print"></i> Print / Save as PDF
                </button>
            </div>
        `;
    }
};

window.addEventListener('DOMContentLoaded', () => {
    App.init();
});
