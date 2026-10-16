/**
 * MediAI Pro — Symptom Checker & Triage Controller
 * Architected by Shashank Dixit
 */

const SymptomChecker = {
    selectedSymptoms: new Set(),
    activeBodySystem: 'All',

    init() {
        this.setupSymptomChips();
        this.setupBodySystemFilter();
        this.setupSymptomSearch();
        this.setupLiveVitals();
        this.setupExampleButtons();
        this.setupDiagnosisForm();
    },

    setupSymptomChips() {
        const chips = document.querySelectorAll('.symptom-chip');
        chips.forEach(chip => {
            chip.addEventListener('click', () => {
                const symId = chip.getAttribute('data-symptom-id');
                if (this.selectedSymptoms.has(symId)) {
                    this.selectedSymptoms.delete(symId);
                    chip.classList.remove('selected');
                } else {
                    this.selectedSymptoms.add(symId);
                    chip.classList.add('selected');
                }
                this.updateSelectedCountBadge();
            });
        });
    },

    updateSelectedCountBadge() {
        const badge = document.getElementById('selected-symptoms-count');
        if (badge) {
            badge.textContent = `${this.selectedSymptoms.size} selected`;
            badge.className = this.selectedSymptoms.size > 0 
                ? "text-xs font-semibold px-2 py-0.5 rounded-full bg-sky-100 text-sky-700 dark:bg-sky-950 dark:text-sky-300"
                : "text-xs text-slate-400";
        }
    },

    setupBodySystemFilter() {
        const buttons = document.querySelectorAll('.body-system-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                buttons.forEach(b => b.classList.remove('active', 'bg-sky-600', 'text-white'));
                btn.classList.add('active', 'bg-sky-600', 'text-white');
                this.activeBodySystem = btn.getAttribute('data-system');
                this.filterSymptomChips();
            });
        });
    },

    setupSymptomSearch() {
        const searchInput = document.getElementById('symptom-search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase().trim();
                const chips = document.querySelectorAll('.symptom-chip');
                chips.forEach(chip => {
                    const text = chip.textContent.toLowerCase();
                    if (!query || text.includes(query)) {
                        chip.classList.remove('hidden');
                    } else {
                        chip.classList.add('hidden');
                    }
                });
            });
        }
    },

    filterSymptomChips() {
        const chips = document.querySelectorAll('.symptom-chip');
        chips.forEach(chip => {
            const system = chip.getAttribute('data-system');
            if (this.activeBodySystem === 'All' || system === this.activeBodySystem) {
                chip.classList.remove('hidden');
            } else {
                chip.classList.add('hidden');
            }
        });
    },

    setupLiveVitals() {
        const heightInput = document.getElementById('vital-height');
        const weightInput = document.getElementById('vital-weight');
        const bmiDisplay = document.getElementById('live-bmi-display');

        const calculateBmi = () => {
            const h = parseFloat(heightInput?.value);
            const w = parseFloat(weightInput?.value);
            if (h > 50 && w > 10) {
                const h_m = h / 100.0;
                const bmi = (w / (h_m * h_m)).toFixed(1);
                let cat = "Normal";
                let color = "text-emerald-600";
                if (bmi < 18.5) { cat = "Underweight"; color = "text-amber-500"; }
                else if (bmi >= 25.0 && bmi < 30.0) { cat = "Overweight"; color = "text-amber-500"; }
                else if (bmi >= 30.0) { cat = "Obese"; color = "text-rose-500"; }
                
                if (bmiDisplay) {
                    bmiDisplay.innerHTML = `<span class="font-bold">${bmi}</span> (${cat})`;
                    bmiDisplay.className = `text-xs font-semibold ${color}`;
                }
            } else if (bmiDisplay) {
                bmiDisplay.innerHTML = `--`;
                bmiDisplay.className = "text-xs text-slate-400";
            }
        };

        if (heightInput && weightInput) {
            heightInput.addEventListener('input', calculateBmi);
            weightInput.addEventListener('input', calculateBmi);
        }
    },

    setupExampleButtons() {
        const exampleButtons = document.querySelectorAll('.load-example-btn');
        exampleButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const exType = btn.getAttribute('data-example');
                this.loadPresetExample(exType);
            });
        });
    },

    loadPresetExample(type) {
        // Clear current selections
        this.selectedSymptoms.clear();
        document.querySelectorAll('.symptom-chip').forEach(c => c.classList.remove('selected'));

        if (type === 'cardiac') {
            document.getElementById('patient-age-input').value = '58';
            document.getElementById('patient-gender-select').value = 'Male';
            document.getElementById('patient-narrative-input').value = 'Crushing chest tightness and pain radiating down the left arm for 45 minutes, accompanied by cold sweat and breathing difficulty.';
            document.getElementById('vital-sys-bp').value = '155';
            document.getElementById('vital-dia-bp').value = '96';
            document.getElementById('vital-hr').value = '104';
            document.getElementById('vital-spo2').value = '94';
            document.getElementById('vital-temp').value = '37.0';
            
            ['chest_pain', 'chest_tightness', 'radiating_arm_pain', 'diaphoresis', 'shortness_of_breath'].forEach(s => {
                this.selectedSymptoms.add(s);
                const chip = document.querySelector(`.symptom-chip[data-symptom-id="${s}"]`);
                if (chip) chip.classList.add('selected');
            });
        } else if (type === 'respiratory') {
            document.getElementById('patient-age-input').value = '42';
            document.getElementById('patient-gender-select').value = 'Female';
            document.getElementById('patient-narrative-input').value = 'High fever, shaking chills, productive cough with greenish-yellow sputum, and sharp right-sided chest pain when breathing in.';
            document.getElementById('vital-sys-bp').value = '118';
            document.getElementById('vital-dia-bp').value = '76';
            document.getElementById('vital-hr').value = '98';
            document.getElementById('vital-spo2').value = '92';
            document.getElementById('vital-temp').value = '38.9';
            
            ['fever', 'chills', 'productive_cough', 'pleuritic_chest_pain', 'shortness_of_breath'].forEach(s => {
                this.selectedSymptoms.add(s);
                const chip = document.querySelector(`.symptom-chip[data-symptom-id="${s}"]`);
                if (chip) chip.classList.add('selected');
            });
        } else if (type === 'appendicitis') {
            document.getElementById('patient-age-input').value = '24';
            document.getElementById('patient-gender-select').value = 'Male';
            document.getElementById('patient-narrative-input').value = 'Started with dull ache near navel, now severe sharp pain localized in the right lower abdomen with nausea and zero appetite.';
            document.getElementById('vital-sys-bp').value = '122';
            document.getElementById('vital-dia-bp').value = '80';
            document.getElementById('vital-hr').value = '92';
            document.getElementById('vital-spo2').value = '99';
            document.getElementById('vital-temp').value = '37.8';
            
            ['abdominal_pain', 'right_lower_quadrant_pain', 'periumbilical_pain', 'nausea', 'anorexia'].forEach(s => {
                this.selectedSymptoms.add(s);
                const chip = document.querySelector(`.symptom-chip[data-symptom-id="${s}"]`);
                if (chip) chip.classList.add('selected');
            });
        } else if (type === 'migraine') {
            document.getElementById('patient-age-input').value = '31';
            document.getElementById('patient-gender-select').value = 'Female';
            document.getElementById('patient-narrative-input').value = 'Intense throbbing headache on right side with nausea, flashing visual spots, and extreme sensitivity to bright light and noise.';
            document.getElementById('vital-sys-bp').value = '115';
            document.getElementById('vital-dia-bp').value = '75';
            document.getElementById('vital-hr').value = '78';
            document.getElementById('vital-spo2').value = '99';
            document.getElementById('vital-temp').value = '36.8';
            
            ['throbbing_headache', 'photophobia', 'phonophobia', 'nausea'].forEach(s => {
                this.selectedSymptoms.add(s);
                const chip = document.querySelector(`.symptom-chip[data-symptom-id="${s}"]`);
                if (chip) chip.classList.add('selected');
            });
        }

        this.updateSelectedCountBadge();
        App.showToast(`Loaded preset scenario: ${type.toUpperCase()}`, 'info');
    },

    setupDiagnosisForm() {
        const form = document.getElementById('diagnosis-form');
        const resetBtn = document.getElementById('reset-symptoms-btn');

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                form.reset();
                this.selectedSymptoms.clear();
                document.querySelectorAll('.symptom-chip').forEach(c => c.classList.remove('selected'));
                this.updateSelectedCountBadge();
                App.showToast('Symptom form cleared.', 'info');
            });
        }

        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.submitDiagnosis();
            });
        }
    },

    async submitDiagnosis() {
        const submitBtn = document.getElementById('run-diagnosis-btn');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing with AI Clinical Engine...`;

        try {
            const ageVal = document.getElementById('patient-age-input').value;
            const genderVal = document.getElementById('patient-gender-select').value;
            const narrativeVal = document.getElementById('patient-narrative-input').value;

            // Comorbidities
            const history = [];
            if (document.getElementById('hist-htn')?.checked) history.push('hypertension');
            if (document.getElementById('hist-dm')?.checked) history.push('diabetes');
            if (document.getElementById('hist-asthma')?.checked) history.push('asthma');
            if (document.getElementById('hist-cad')?.checked) history.push('cad');

            const isSmoker = document.getElementById('hist-smoker')?.checked || false;
            const isPregnant = document.getElementById('hist-pregnant')?.checked || false;

            // Vitals
            const vitals = {
                systolic_bp: document.getElementById('vital-sys-bp')?.value || null,
                diastolic_bp: document.getElementById('vital-dia-bp')?.value || null,
                heart_rate: document.getElementById('vital-hr')?.value || null,
                spo2: document.getElementById('vital-spo2')?.value || null,
                temperature: document.getElementById('vital-temp')?.value || null,
                respiratory_rate: document.getElementById('vital-rr')?.value || null,
                glucose: document.getElementById('vital-glucose')?.value || null,
                height_cm: document.getElementById('vital-height')?.value || null,
                weight_kg: document.getElementById('vital-weight')?.value || null
            };

            const payload = {
                age: ageVal ? parseInt(ageVal) : null,
                gender: genderVal,
                narrative: narrativeVal,
                symptoms: Array.from(this.selectedSymptoms),
                body_system: this.activeBodySystem,
                history: history,
                smoking: isSmoker,
                pregnant: isPregnant,
                vitals: vitals,
                api_key: App.apiKey || null
            };

            const response = await fetch('/api/diagnose', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`HTTP status ${response.status}`);
            }

            const resJson = await response.json();
            if (resJson.success && resJson.data) {
                App.latestDiagnosisData = resJson.data;
                this.renderResults(resJson.data);
                App.showToast('Clinical analysis complete!', 'success');
            } else {
                throw new Error("Invalid response format");
            }
        } catch (err) {
            console.error("Diagnosis error:", err);
            App.showToast(`Analysis failed: ${err.message}`, 'danger');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    },

    renderResults(data) {
        const resultsContainer = document.getElementById('diagnosis-results-container');
        if (!resultsContainer) return;

        resultsContainer.classList.remove('hidden');

        // Urgency Colors
        const urgencyConfig = {
            'Emergency': {
                bg: 'bg-rose-50 dark:bg-rose-950/40 border-rose-300 dark:border-rose-800 text-rose-800 dark:text-rose-200',
                badge: 'bg-rose-600 text-white',
                icon: 'fa-triangle-exclamation'
            },
            'Urgent': {
                bg: 'bg-amber-50 dark:bg-amber-950/40 border-amber-300 dark:border-amber-800 text-amber-800 dark:text-amber-200',
                badge: 'bg-amber-600 text-white',
                icon: 'fa-circle-exclamation'
            },
            'Routine': {
                bg: 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200',
                badge: 'bg-emerald-600 text-white',
                icon: 'fa-circle-check'
            }
        };

        const uStyle = urgencyConfig[data.overall_urgency] || urgencyConfig['Routine'];
        const primary = data.primary_diagnosis;

        resultsContainer.innerHTML = `
            <!-- Triage Urgency Header Banner -->
            <div class="p-5 rounded-2xl border ${uStyle.bg} flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6 shadow-sm">
                <div class="flex items-center gap-3">
                    <span class="w-10 h-10 rounded-full flex items-center justify-center text-lg ${uStyle.badge}">
                        <i class="fa-solid ${uStyle.icon}"></i>
                    </span>
                    <div>
                        <div class="text-xs uppercase tracking-wider font-bold">Clinical Triage Classification</div>
                        <div class="text-xl font-black">${data.overall_urgency} Level</div>
                    </div>
                </div>
                <div class="text-xs">
                    <div>NEWS2 Early Warning Score: <strong>${data.vital_assessment?.news2_score ?? 0}</strong></div>
                    <div>Biometric Risk: <strong>${data.vital_assessment?.vital_triage || 'Stable'}</strong></div>
                </div>
            </div>

            <!-- Primary Working Diagnosis -->
            <div class="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm mb-6">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-3">
                    <div>
                        <div class="text-xs font-bold text-sky-600 uppercase tracking-wider">Primary Working Diagnosis</div>
                        <h2 class="text-2xl font-black text-slate-900 dark:text-white">${primary.name}</h2>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-mono text-xs font-bold rounded-lg border border-slate-200 dark:border-slate-700">
                            ICD-10: ${primary.icd10}
                        </span>
                        <span class="px-3 py-1 bg-sky-600 text-white text-xs font-black rounded-lg shadow-sm">
                            ${primary.probability}% Match
                        </span>
                    </div>
                </div>

                <!-- Match Confidence Progress Bar -->
                <div class="w-full bg-slate-100 dark:bg-slate-800 h-2.5 rounded-full overflow-hidden mb-4">
                    <div class="bg-gradient-to-r from-sky-500 to-indigo-600 h-full rounded-full transition-all duration-700" style="width: ${primary.probability}%"></div>
                </div>

                <p class="text-sm text-slate-600 dark:text-slate-300 leading-relaxed mb-4">${primary.description}</p>

                <!-- Matched Symptoms Tags -->
                ${primary.matched_primary_symptoms?.length > 0 ? `
                <div class="pt-3 border-t border-slate-100 dark:border-slate-800">
                    <div class="text-xs font-semibold text-slate-500 mb-2">Correlated Chief Symptoms:</div>
                    <div class="flex flex-wrap gap-1.5">
                        ${primary.matched_primary_symptoms.map(s => `
                            <span class="px-2 py-0.5 bg-sky-50 dark:bg-sky-950/40 text-sky-700 dark:text-sky-300 border border-sky-200 dark:border-sky-800/60 rounded-md text-xs font-medium">
                                <i class="fa-solid fa-check text-[10px] mr-1"></i> ${s}
                            </span>
                        `).join('')}
                    </div>
                </div>
                ` : ''}
            </div>

            <!-- Red Flag Warnings (If present) -->
            ${data.red_flags?.length > 0 ? `
            <div class="p-5 bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/60 rounded-2xl mb-6">
                <h4 class="text-sm font-bold text-rose-800 dark:text-rose-300 flex items-center gap-2 mb-2">
                    <i class="fa-solid fa-triangle-exclamation"></i> Identified Red Flags & Critical Alerts
                </h4>
                <ul class="list-disc list-inside text-xs text-rose-700 dark:text-rose-400 space-y-1">
                    ${data.red_flags.map(rf => `<li>${rf}</li>`).join('')}
                </ul>
            </div>
            ` : ''}

            <!-- Differential Diagnoses -->
            ${data.differential_diagnoses?.length > 0 ? `
            <div class="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm mb-6">
                <h3 class="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
                    <i class="fa-solid fa-code-compare text-indigo-600"></i> Differential Diagnoses Considered
                </h3>
                <div class="space-y-3">
                    ${data.differential_diagnoses.map(diff => `
                        <div class="p-3.5 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700/60">
                            <div class="flex justify-between items-center mb-1.5">
                                <span class="font-bold text-sm text-slate-800 dark:text-slate-200">${diff.name}</span>
                                <span class="text-xs font-bold text-slate-500">${diff.probability}%</span>
                            </div>
                            <div class="w-full bg-slate-200 dark:bg-slate-700 h-1.5 rounded-full overflow-hidden mb-2">
                                <div class="bg-indigo-500 h-full rounded-full" style="width: ${diff.probability}%"></div>
                            </div>
                            <div class="text-xs text-slate-500 dark:text-slate-400 flex items-center justify-between">
                                <span>System: ${diff.system}</span>
                                <span class="font-mono">ICD-10: ${diff.icd10}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}

            <!-- Two-Column Next Steps: Recommended Tests & Management -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <!-- Recommended Diagnostics -->
                <div class="p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm">
                    <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-3">
                        <i class="fa-solid fa-microscope text-teal-600"></i> Recommended Diagnostic Tests
                    </h4>
                    <ul class="space-y-2 text-xs text-slate-600 dark:text-slate-300">
                        ${data.recommended_tests.map(test => `
                            <li class="flex items-start gap-2">
                                <i class="fa-solid fa-circle-arrow-right text-teal-500 mt-0.5"></i>
                                <span>${test}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>

                <!-- Clinical Management & Home Care -->
                <div class="p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm">
                    <h4 class="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-3">
                        <i class="fa-solid fa-hand-holding-medical text-sky-600"></i> Care Guidance & Next Steps
                    </h4>
                    <ul class="space-y-2 text-xs text-slate-600 dark:text-slate-300">
                        ${data.clinical_management.map(care => `
                            <li class="flex items-start gap-2">
                                <i class="fa-solid fa-check text-sky-500 mt-0.5"></i>
                                <span>${care}</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>

            <!-- Action Bar -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 bg-slate-50 dark:bg-slate-800/40 rounded-2xl border border-slate-200 dark:border-slate-700/60">
                <div class="text-xs text-slate-500 dark:text-slate-400">
                    <i class="fa-solid fa-shield-halved text-sky-600 mr-1"></i>
                    Engine: <strong>${data.ai_powered_by}</strong>
                </div>
                <button onclick="App.switchTab('report-tab')" class="px-5 py-2.5 bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold rounded-xl shadow-md transition flex items-center gap-2">
                    <i class="fa-solid fa-file-medical"></i> View & Print Full Medical Report
                </button>
            </div>
        `;

        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
};

window.addEventListener('DOMContentLoaded', () => {
    SymptomChecker.init();
});
