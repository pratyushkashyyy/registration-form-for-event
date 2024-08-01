document.addEventListener('DOMContentLoaded', () => {
    const participantTypeRadios = document.querySelectorAll('input[name="participant_type"]');
    const collegeNameBox = document.getElementById('college-name-box');
    const eventRadios = document.querySelectorAll('input[name="event"]');
    
    // Show/hide college name input based on participant type
    participantTypeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (document.querySelector('input[name="participant_type"]:checked')?.value === 'Other') {
                collegeNameBox.classList.remove('hidden');
            } else {
                collegeNameBox.classList.add('hidden');
            }
        });
    });

    // Update price and team members when event changes
    eventRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            updatePrice();
            updateTeamMembers();
        });
    });
});

function showStep(stepNumber) {
    const steps = ['step1', 'step2', 'step3', 'step4'];
    steps.forEach((step, index) => {
        document.getElementById(step).classList.toggle('hidden', index + 1 !== stepNumber);
    });
}

function updatePrice() {
    const participantType = document.querySelector('input[name="participant_type"]:checked')?.value;
    const event = document.querySelector('input[name="event"]:checked')?.value;
    let price = 0;

    if (participantType && event) {
        const priceMap = {
            'Jain': {
                'BGMI': 299,
                'Valorant': 299,
                'Blazing Tongue': 99,
                'IT-Quiz': 99,
                'Pixel-Perfect': 99,
                'Meme-Mania': 99,
                'CTF': 199,
                'Web-Wizards': 149,
                'Scam-Poetry': 149,
                'Jury-Rigged': 249,
                'Ideathon': 249
            },
            'Other': {
                'BGMI': 299,
                'Valorant': 299,
                'Ideathon': 299,
                'Jury-Rigged': 299,
                'Blazing Tongue': 149,
                'IT-Quiz': 149,
                'Pixel-Perfect': 149,
                'Meme-Mania': 149,
                'CTF': 249,
                'Web-Wizards': 199,
                'Scam-Poetry': 199
            }
        };
        
        price = priceMap[participantType]?.[event] || "Event not found";
    } else {
        price = "Select or Enter Your College Name";
    }

    document.getElementById('price-display').textContent = price;
}

function updateTeamMembers() {
    const selectedEvent = document.querySelector('input[name="event"]:checked');
    const teamGrid = document.getElementById('team-grid');
    teamGrid.innerHTML = '';

    if (selectedEvent) {
        let memberCount = 1;
        switch (selectedEvent.value) {
            case 'BGMI':
                memberCount = 4;
                break;
            case 'Valorant':
                memberCount = 5;
                break;
            case 'CTF':
                memberCount = 3;
                break;
            default:
                memberCount = 1;
                break;
        }

        for (let i = 0; i < memberCount; i++) {
            const div = document.createElement('div');
            div.classList.add('input_box', 'double');
            div.innerHTML = `
                <label for="member${i + 1}">Member ${i + 1} Name:</label>
                <input type="text" id="member${i + 1}" name="team_member_${i + 1}" placeholder="Enter member ${i + 1} name" required>
            `;
            teamGrid.appendChild(div);
        }
    }
}

// Navigation buttons
document.addEventListener('click', (event) => {
    if (event.target.closest('.pay-button, .previous-button')) {
        const currentStep = document.querySelector('.step:not(.hidden)');
        const stepActions = {
            'step1': showStep.bind(null, 2),
            'step2': showStep.bind(null, 3),
            'step3': showStep.bind(null, 4),
            'step4': () => document.getElementById('registrationForm').submit()
        };

        if (event.target.closest('.pay-button')) {
            // Next button functionality
            if (event.target.closest('.pay-button').textContent.includes('Next')) {
                stepActions[currentStep.id]?.();
            }
        } else if (event.target.closest('.previous-button')) {
            // Previous button functionality
            const prevStepActions = {
                'step2': showStep.bind(null, 1),
                'step3': showStep.bind(null, 2),
                'step4': showStep.bind(null, 3)
            };
            prevStepActions[currentStep.id]?.();
        }
    }
});




document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm');

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the form from submitting immediately

        // You can add additional validation logic here if needed

        // Show a confirmation dialog
        Swal.fire({
            title: 'Are you sure?',
            text: "Do you want to submit the form?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, submit it!'
        }).then((result) => {
            if (result.isConfirmed) {
                // If confirmed, submit the form programmatically
                form.submit();
            }
        });
    });
});
