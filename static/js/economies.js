document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.getElementById("economiesTableBody");
    const chartCanvas = document.getElementById("economiesChart").getContext("2d");

    fetch("/api/Economies")
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP ! statut : ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Vérifier si l'élément pour insérer les données existe
            if (!tableBody) {
                console.error("L'élément avec l'id 'economiesTableBody' est introuvable.");
                return;
            }

            // Insérer les données dans le tableau
            data.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.type_facture}</td>
                    <td>${item.montant_passe ? item.montant_passe.toFixed(2) : 0.00}</td>
                    <td>${item.montant_actuel ? item.montant_actuel.toFixed(2) : 0.00}</td>
                    <td style="color: ${item.economie >= 0 ? 'green' : 'red'};">${item.economie ? item.economie.toFixed(2) : 0.00}</td>
                `;
                tableBody.appendChild(row);
            });

            // Générer un graphique
            const chartData = {
                labels: data.map(item => item.type_facture),
                datasets: [
                    {
                        label: "Montant Passé (€)",
                        data: data.map(item => item.montant_passe),
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1
                    },
                    {
                        label: "Montant Actuel (€)",
                        data: data.map(item => item.montant_actuel),
                        backgroundColor: "rgba(255, 99, 132, 0.2)",
                        borderColor: "rgba(255, 99, 132, 1)",
                        borderWidth: 1
                    }
                ]
            };

            new Chart(chartCanvas, {
                type: "bar",
                data: chartData,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "top",
                        },
                        title: {
                            display: true,
                            text: "Comparaison des Consommations Passées et Actuelles"
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error("Erreur lors du chargement des données :", error);
        });
});
