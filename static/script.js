async function sendSOS() {

    const status = document.getElementById("sosStatus");

    try {

        const response = await fetch("/sos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                latitude: currentLatitude,
                longitude: currentLongitude
            })
        });

        const data = await response.json();

        if (data.success) {

            const phone = document.getElementById("contactPhone")
                .value.trim();

            const mapLink =
                "https://www.google.com/maps?q=" +
                currentLatitude + "," + currentLongitude;

            const message =
                "🚨 EMERGENCY SOS! I need help.\n\n" +
                "📍 My current location:\n" +
                mapLink;

            status.innerHTML =
                "🚨 SOS ACTIVATED<br>" +
                "📍 Location received<br>" +
                "📱 Opening emergency SMS...";

            // Save location to server
            saveLocationToServer();

            // Open the phone's SMS application
            if (phone) {

                setTimeout(function () {

                    window.location.href =
                        "sms:" + phone +
                        "?body=" +
                        encodeURIComponent(message);

                }, 500);

            } else {

                status.innerHTML +=
                    "<br>⚠️ Please enter an emergency phone number first.";
            }

        } else {

            status.innerHTML = "❌ SOS failed";
        }

    } catch (error) {

        console.error("SOS error:", error);

        status.innerHTML =
            "❌ SOS server connection error";
    }
}