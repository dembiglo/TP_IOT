document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#economiesTable tbody");
    const chartCanvas = document.getElementById("economiesChart");

    // Charger les données des économies depuis l'API
    fetch("/api/Economies")
        .then(response => response.json())
        .then(data => {
            // Mettre à jour le tableau
            tableBody.innerHTML = data.map(item => `
                <tr>
                    <td>${item.type_facture}</td>
                    <td>${item.montant_passe.toFixed(2)}</td>
                    <td>${item.montant_actuel.toFixed(2)}</td>
                    <td>${item.economie.toFixed(2)}</td>
                </tr>
            `).join("");

            // Créer le graphique
            const chartData = {
                labels: data.map(item => item.type_facture),
                datasets: [
                    {
                        label: "Montant Passé (€)",
                        data: data.map(item => item.montant_passe),
                        backgroundColor: "rgba(75, 192, 192, 0.6)"
                    },
                    {
                        label: "Montant Actuel (€)",
                        data: data.map(item => item.montant_actuel),
                        backgroundColor: "rgba(255, 99, 132, 0.6)"
                    },
                    {
                        label: "Économie (€)",
                        data: data.map(item => item.economie),
                        backgroundColor: "rgba(54, 162, 235, 0.6)"
                    }
                ]
            };

            new Chart(chartCanvas, {
                type: "bar",
                data: chartData,
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Erreur lors du chargement des données :", error));
});
