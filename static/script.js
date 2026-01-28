document.addEventListener('DOMContentLoaded', () => {
    // Tabs
    const tabs = document.querySelectorAll('.tab-btn');
    const inputGroups = document.querySelectorAll('.input-group');
    let currentMode = 'text';

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            inputGroups.forEach(g => g.classList.remove('active'));
            
            tab.classList.add('active');
            const target = tab.getAttribute('data-tab');
            document.getElementById(`${target}-input`).classList.add('active');
            currentMode = target;
        });
    });

    // Image Upload Click
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.querySelector('input[type="file"]');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            uploadArea.querySelector('p').textContent = `Selected: ${e.target.files[0].name}`;
        }
    });

    // Analyze
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');
    const loader = document.querySelector('.loader');
    const resultsContent = document.querySelector('.results-content');
    
    analyzeBtn.addEventListener('click', async () => {
        // Prepare payload
        let payload = {};
        
        if (currentMode === 'text') {
            const text = document.querySelector('#text-input textarea').value;
            if (!text) return alert("Please enter text.");
            payload = { text: text };
        } else if (currentMode === 'url') {
            const url = document.querySelector('#url-input input').value;
            if (!url) return alert("Please enter a URL.");
            payload = { url: url };
        } else if (currentMode === 'image') {
            const file = fileInput.files[0];
            if (!file) return alert("Please upload an image.");
            // Convert to base64
            const reader = new FileReader();
            reader.onload = async () => {
                const b64 = reader.result;
                payload = { image: b64 };
                await performAnalysis(payload);
            };
            reader.readAsDataURL(file);
            return; // performAnalysis called in callback
        }

        await performAnalysis(payload);
    });

    async function performAnalysis(payload) {
        // UI State
        resultsSection.classList.remove('hidden');
        loader.classList.remove('hidden');
        resultsContent.classList.add('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error("Analysis failed");
            
            const data = await response.json();
            renderResults(data);

        } catch (error) {
            console.error(error);
            alert("An error occurred during analysis: " + error.message);
        } finally {
            loader.classList.add('hidden');
        }
    }

    function renderResults(data) {
        resultsContent.classList.remove('hidden');
        
        // Score
        const score = Math.round(data.credibility_score);
        const scoreVal = document.getElementById('score-value');
        const scoreCircle = document.getElementById('score-circle');
        const badge = document.getElementById('score-badge');
        
        // Update number animation (simple text update for now)
        scoreVal.textContent = score;
        
        // Update circle stroke
        const radius = 54;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (score / 100) * circumference;
        scoreCircle.style.strokeDasharray = `${circumference} ${circumference}`;
        scoreCircle.style.strokeDashoffset = offset;
        
        // Update badge color
        if (score >= 80) {
            badge.textContent = "Strong Support";
            badge.style.color = "#3fb950";
            badge.style.borderColor = "rgba(63, 185, 80, 0.3)";
            scoreCircle.style.stroke = "#3fb950";
        } else if (score >= 50) {
            badge.textContent = "Moderate Support";
            badge.style.color = "#d29922";
            badge.style.borderColor = "rgba(210, 153, 34, 0.3)";
            scoreCircle.style.stroke = "#d29922";
        } else {
            badge.textContent = "Low Support";
            badge.style.color = "#f85149";
            badge.style.borderColor = "rgba(248, 81, 73, 0.3)";
            scoreCircle.style.stroke = "#f85149";
        }

        // Text
        document.getElementById('score-explanation').textContent = data.explanation;

        // Sources
        const list = document.getElementById('sources-list');
        list.innerHTML = '';
        
        if (data.supporting_sources.length === 0) {
            list.innerHTML = '<p style="color:var(--text-secondary)">No supporting sources found.</p>';
        } else {
            data.supporting_sources.forEach(src => {
                const div = document.createElement('div');
                div.className = `source-item ${src.similarity_score >= 0.7 ? 'high-sim' : 'med-sim'}`;
                
                div.innerHTML = `
                    <div class="source-header">
                        <span class="source-domain">${src.domain || 'Source'}</span>
                        <span class="source-sim">${Math.round(src.similarity_score * 100)}% Match</span>
                    </div>
                    <div class="source-summary">${src.summary}</div>
                    <a href="${src.source_url}" target="_blank" class="source-link">Read Source <i class="fa-solid fa-external-link-alt" style="font-size:0.7em"></i></a>
                `;
                list.appendChild(div);
            });
        }
    }
});
