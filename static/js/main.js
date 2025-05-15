// Initialize Select2 for better dropdown experience
$(document).ready(function() {
    $('#championSelect').select2({
        placeholder: 'Select a champion...',
        allowClear: true
    });

    $('#regionSelect').select2({
        placeholder: 'Select regions...',
        allowClear: true
    });

    // Load initial data
    loadRegions();
    loadChampions();
});

// Load available regions
async function loadRegions() {
    try {
        const response = await fetch('/api/regions');
        const regions = await response.json();
        
        const regionSelect = $('#regionSelect');
        regionSelect.empty();
        
        regions.forEach(region => {
            regionSelect.append(new Option(region, region));
        });
    } catch (error) {
        console.error('Error loading regions:', error);
    }
}

// Load champion list
async function loadChampions() {
    try {
        const response = await fetch('/api/champions');
        const champions = await response.json();
        
        const championSelect = $('#championSelect');
        championSelect.empty();
        championSelect.append(new Option('Select a champion...', ''));
        
        Object.keys(champions).forEach(champion => {
            championSelect.append(new Option(champion, champion));
        });
    } catch (error) {
        console.error('Error loading champions:', error);
    }
}

// Handle champion selection
$('#championSelect').on('change', function() {
    const selectedChampion = $(this).val();
    if (selectedChampion) {
        loadChampionData(selectedChampion);
    } else {
        clearChampionData();
    }
});

// Load champion data
async function loadChampionData(championName) {
    try {
        const [championResponse, analysisResponse] = await Promise.all([
            fetch(`/api/champion/${championName}`),
            fetch(`/api/analysis/${championName}`)
        ]);

        const championData = await championResponse.json();
        const analysisData = await analysisResponse.json();

        updateChampionDisplay(championData, analysisData);
    } catch (error) {
        console.error('Error loading champion data:', error);
    }
}

// Update the display with champion data
function updateChampionDisplay(championData, analysisData) {
    // Update winrate chart
    updateWinrateChart(championData);
    
    // Update analysis content
    updateAnalysisContent(analysisData);
    
    // Update statistics content
    updateStatisticsContent(analysisData.statistics);
}

// Update winrate chart
function updateWinrateChart(championData) {
    const regions = Object.keys(championData.regions);
    const winrates = regions.map(region => championData.regions[region].winrate);

    const trace = {
        x: regions,
        y: winrates,
        type: 'bar',
        marker: {
            color: winrates.map(rate => rate > 0.5 ? '#28a745' : '#dc3545')
        }
    };

    const layout = {
        title: `${championData.name} Winrate by Region`,
        yaxis: {
            title: 'Winrate',
            range: [0.4, 0.6],
            tickformat: '.1%'
        },
        margin: {
            l: 50,
            r: 50,
            b: 100,
            t: 50,
            pad: 4
        }
    };

    Plotly.newPlot('winrateChart', [trace], layout);
}

// Update analysis content
function updateAnalysisContent(analysisData) {
    const analysisContent = $('#analysisContent');
    analysisContent.empty();

    analysisData.insights.forEach(insight => {
        analysisContent.append(`
            <div class="insight-item">
                ${insight}
            </div>
        `);
    });
}

// Update statistics content
function updateStatisticsContent(statistics) {
    const statisticsContent = $('#statisticsContent');
    statisticsContent.empty();

    const stats = [
        { label: 'Mean Winrate', value: formatPercentage(statistics.mean_winrate) },
        { label: 'Standard Deviation', value: formatPercentage(statistics.std_winrate) },
        { label: 'Highest Winrate', value: `${formatPercentage(statistics.max_winrate)} (${statistics.max_region})` },
        { label: 'Lowest Winrate', value: `${formatPercentage(statistics.min_winrate)} (${statistics.min_region})` }
    ];

    stats.forEach(stat => {
        statisticsContent.append(`
            <div class="stat-item">
                <span>${stat.label}</span>
                <span>${stat.value}</span>
            </div>
        `);
    });
}

// Clear champion data display
function clearChampionData() {
    $('#winrateChart').empty();
    $('#analysisContent').html('<p class="text-muted">Select a champion to view analysis</p>');
    $('#statisticsContent').html('<p class="text-muted">Select a champion to view statistics</p>');
}

// Format percentage
function formatPercentage(value) {
    return (value * 100).toFixed(1) + '%';
} 