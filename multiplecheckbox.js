
document.addEventListener("DOMContentLoaded", function () {
    const selectAll = document.getElementById("select-all");
    const checkboxes = document.querySelectorAll(".row-checkbox");
    const actionButtons = document.getElementById("action-buttons");
    const sendSMSBtn = document.getElementById("send-sms-btn");

    const modal = document.getElementById("smsModal");
    const closeModal = document.getElementById("closeModal");
    const submitSms = document.getElementById("submitSms");
    const smsMessage = document.getElementById("smsMessage");
    const loader = document.getElementById("loader");
    const modalMessage = document.getElementById("modalMessage");

    // Toggle action buttons based on checkbox selection
    function toggleActionButtons() {
        const anyChecked = Array.from(checkboxes).some(cb => cb.checked);
        actionButtons.style.display = anyChecked ? "block" : "none";

        const allChecked = Array.from(checkboxes).every(cb => cb.checked);
        const someChecked = Array.from(checkboxes).some(cb => cb.checked);
     

        selectAll.checked = allChecked;
        selectAll.indeterminate = !allChecked && someChecked;
    }

    if (selectAll) {
        selectAll.addEventListener("change", function () {
            checkboxes.forEach(cb => cb.checked = selectAll.checked);
            toggleActionButtons();
        });
    }

    checkboxes.forEach(cb => cb.addEventListener("change", toggleActionButtons));

    // Open modal when "Send SMS" is clicked
    sendSMSBtn.addEventListener("click", function () {
        const selectedIds = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        if (selectedIds.length === 0) {
            alert("Please select at least one contact.");
            return;
        }
        modal.style.display = "block";
        modalMessage.style.display = "none";
    });

    // Close modal on cancel
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Send SMS logic


    submitSms.addEventListener("click", function () {
    const selectedIds = Array.from(checkboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
    const messageText = smsMessage.value.trim();

    modalMessage.style.display = "none";

    if (messageText === "") {
        modalMessage.textContent = "Please enter a message before sending...";
        modalMessage.style.color = "red";
        modalMessage.style.display = "block";
        return;
    }

    loader.style.display = "block";
    submitSms.style.display = "none";
    closeModal.style.display = "none";

    // Create a promise that resolves after 2 seconds
    const delay = new Promise(resolve => setTimeout(resolve, 2000));

    // Create the fetch promise
    const fetchPromise = fetch("{% url 'bulk_send_sms' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}",
        },
        body: JSON.stringify({ contact_ids: selectedIds, message: messageText })
    }).then(response => response.json());

    // Wait for both fetch and delay to complete
    Promise.all([fetchPromise, delay])
        .then(([data]) => {
            loader.style.display = "none";
            if (data.success) {
                modalMessage.textContent = "SMS sent successfully!";
                modalMessage.style.color = "green";
                modalMessage.style.display = "block";

                setTimeout(() => {
                    modal.style.display = "none";
                    location.reload();
                }, 2000);
            } else {
                modalMessage.textContent = "Failed to send SMS.";
                modalMessage.style.color = "red";
                modalMessage.style.display = "block";
                submitSms.style.display = "block";
                closeModal.style.display = "block";
            }
        })
        .catch(err => {
            loader.style.display = "none";
            modalMessage.textContent = "An error occurred. Please try again.";
            modalMessage.style.color = "red";
            modalMessage.style.display = "block";
            submitSms.style.display = "block";
            closeModal.style.display = "block";
            console.error("SMS send error:", err);
        });
});

});

