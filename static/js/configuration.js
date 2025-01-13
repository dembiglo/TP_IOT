document.addEventListener("DOMContentLoaded", () => {
    const capteursTable = document.getElementById("capteursTable");
    const addCapteurForm = document.getElementById("addCapteurForm");

    // Charger les capteurs/actionneurs
    async function loadCapteurs() {
        try {
            const response = await fetch("/api/Capteurs");
            if (!response.ok) throw new Error("Erreur lors du chargement des capteurs");
            const capteurs = await response.json();

            capteursTable.innerHTML = "";
            capteurs.forEach(capteur => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${capteur.id_capteur}</td>
                    <td>${capteur.id_type}</td>
                    <td>${capteur.reference_commerciale}</td>
                    <td>${capteur.id_piece}</td>
                    <td>${capteur.port_communication}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" onclick="editCapteur(${capteur.id_capteur}, '${capteur.id_type}', '${capteur.reference_commerciale}', '${capteur.id_piece}', '${capteur.port_communication}')">Modifier</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteCapteur(${capteur.id_capteur})">Supprimer</button>
                    </td>
                `;
                capteursTable.appendChild(row);
            });
        } catch (error) {
            console.error("Erreur :", error);
        }
    }

    // Ajouter ou modifier un capteur/actionneur
    addCapteurForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const id = document.getElementById("capteurId")?.value || null;
        const newCapteur = {
            id_type: document.getElementById("addType").value,
            reference_commerciale: document.getElementById("addReference").value,
            id_piece: document.getElementById("addPiece").value,
            port_communication: document.getElementById("addPort").value,
        };

        try {
            const response = await fetch(id ? `/api/Capteurs/${id}` : "/api/Capteurs", {
                method: id ? "PUT" : "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(newCapteur),
            });
            if (!response.ok) throw new Error("Erreur lors de l'ajout ou de la mise à jour");
            loadCapteurs();
            addCapteurForm.reset();
        } catch (error) {
            console.error("Erreur :", error);
        }
    });

    // Supprimer un capteur/actionneur
    window.deleteCapteur = async function (id) {
        try {
            const response = await fetch(`/api/Capteurs/${id}`, { method: "DELETE" });
            if (!response.ok) throw new Error("Erreur lors de la suppression");
            loadCapteurs();
        } catch (error) {
            console.error("Erreur :", error);
        }
    };

    // Pré-remplir le formulaire pour modifier
    window.editCapteur = function (id, type, reference, piece, port) {
        document.getElementById("capteurId").value = id;
        document.getElementById("addType").value = type;
        document.getElementById("addReference").value = reference;
        document.getElementById("addPiece").value = piece;
        document.getElementById("addPort").value = port;
    };

    // Charger les capteurs/actionneurs au chargement de la page
    loadCapteurs();
});
