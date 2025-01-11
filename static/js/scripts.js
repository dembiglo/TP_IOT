document.addEventListener("DOMContentLoaded", async () => {
    const timeFilter = document.getElementById('timeFilter');
    const consumptionChartElement = document.getElementById('consumptionChart');
    let consumptionChart;

    async function fetchFactures(period) {
        try {
            const response = await fetch('/api/Facture');
            if (!response.ok) {
                throw new Error('Erreur lors de la récupération des données');
            }
            const factures = await response.json();

            // Regrouper les factures par type et période
            const groupedData = {};
            factures.forEach(facture => {
                const date = new Date(facture.date_facture);
                let periodLabel;

                if (period === 'day') {
                    periodLabel = date.toISOString().split('T')[0]; // Format YYYY-MM-DD
                } else if (period === 'month') {
                    periodLabel = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
                } else if (period === 'year') {
                    periodLabel = `${date.getFullYear()}`;
                }

                if (!groupedData[periodLabel]) {
                    groupedData[periodLabel] = {};
                }

                if (!groupedData[periodLabel][facture.type_facture]) {
                    groupedData[periodLabel][facture.type_facture] = 0;
                }

                groupedData[periodLabel][facture.type_facture] += facture.valeur_consommee;
            });

            // Préparer les données pour le graphique
            const labels = Object.keys(groupedData);
            const datasets = [
                'Electricité', 'Eau', 'Déchets', 'Assurance', 'Internet', 'Gaz', 'Loyer'
            ].map(type => {
                return {
                    label: type,
                    data: labels.map(label => groupedData[label][type] || 0),
                    borderColor: getRandomColor(),
                    backgroundColor: getRandomColor(0.2),
                };
            });

            return { labels, datasets };

        } catch (error) {
            console.error('Erreur :', error);
            return null;
        }
    }

    function getRandomColor(alpha = 1) {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    function updateChart(data) {
        if (!data) return;

        if (consumptionChart) {
            consumptionChart.destroy();
        }

        consumptionChart = new Chart(consumptionChartElement, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: `Consommation des factures (${timeFilter.value})`
                    }
                }
            },
        });
    }

    async function updateConsumptionChart() {
        const period = timeFilter.value;
        const chartData = await fetchFactures(period);
        updateChart(chartData);
    }

    timeFilter.addEventListener('change', updateConsumptionChart);

    // Initial load
    updateConsumptionChart();
});
