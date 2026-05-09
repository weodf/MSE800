# Clinic System Activity Diagram Description

## Overview

This activity diagram describes a simplified New Zealand-style clinic system workflow.  
The process allows a patient to book an appointment with a GP or clinic, pay the booking or consultation fee, attend the consultation, and order medication if a prescription is required.

The diagram is divided into two main swimlanes:

- **Patient**
- **GP / Clinic System**

The patient performs actions such as selecting a clinic, choosing an appointment time, paying the fee, attending the consultation, and selecting a pharmacy.  
The GP / Clinic system handles enrolment checking, appointment availability, payment confirmation, consultation recording, prescription issuing, and medication order processing.

---

## Phase 1: Appointment Booking

The process starts when the patient selects a GP clinic or an online GP service.

The GP / Clinic system then checks the patient's enrolment status. This reflects a common New Zealand healthcare process, where patients may be enrolled with a specific GP practice.

After the enrolment check, the patient chooses the appointment type, such as a GP consultation, nurse consultation, or online consultation. The patient then selects a preferred date and time.

The system checks whether the selected appointment slot is available.

If the slot is not available, the patient is redirected to choose another appointment type or time.

If the slot is available, the system calculates the booking or consultation fee.

---

## Phase 2: Payment and Appointment Confirmation

After the consultation fee is calculated, the patient pays the booking or consultation fee.

The GP / Clinic system checks whether the payment is successful.

If the payment fails, the patient is asked to pay again.

If the payment is successful, the GP / Clinic system confirms the appointment.

At this point, the appointment booking process is complete.

---

## Phase 3: Consultation

After the appointment is confirmed, the patient attends the consultation.

The doctor or nurse conducts the consultation and records the patient's condition.

The system then checks whether a prescription is needed.

If no prescription is required, the GP / Clinic system records the consultation notes, and the process ends.

If a prescription is required, the doctor issues an electronic prescription.

---

## Phase 4: Medication Order

After the electronic prescription is issued, the patient selects a preferred pharmacy.

The GP / Clinic system sends the prescription to the selected pharmacy.

The system then processes the medication order.

Once the medication order is processed, the patient receives a pickup or delivery notification.

The process ends after the medication order is completed.

---

## Summary

This activity diagram shows the full patient journey from appointment booking to medication ordering.

The main workflow includes:

1. Selecting a GP clinic or online GP service
2. Choosing an appointment type and time
3. Checking appointment availability
4. Paying the booking or consultation fee
5. Confirming the appointment
6. Attending the consultation
7. Issuing an electronic prescription if needed
8. Selecting a preferred pharmacy
9. Processing the medication order
10. Receiving pickup or delivery notification

The design is simple enough for an academic activity diagram, while still reflecting key features of a New Zealand clinic workflow, such as GP enrolment checking and electronic prescriptions.
