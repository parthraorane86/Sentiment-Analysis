/**
 * main.js - Client-side JavaScript for Complaint Management System
 * Handles: character counter, example-text injection, form validation,
 *          and submit button loading state.
 */

document.addEventListener("DOMContentLoaded", function () {

  // ------------------------------------------------------------------
  // 1. CHARACTER COUNTER for the review textarea
  // ------------------------------------------------------------------
  const textarea  = document.getElementById("review_text");
  const charCount = document.getElementById("char-count");

  if (textarea && charCount) {
    // Update on every keystroke
    textarea.addEventListener("input", function () {
      const len = this.value.length;
      charCount.textContent = len;

      // Warn visually when approaching the limit
      if (len > 900) {
        charCount.style.color = "#ef4444";
      } else {
        charCount.style.color = "";
      }
    });
  }


  // ------------------------------------------------------------------
  // 2. EXAMPLE REVIEW BUTTONS — inject text into the textarea
  // ------------------------------------------------------------------
  const exampleBtns = document.querySelectorAll(".example-btn");

  exampleBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const sampleText = this.getAttribute("data-text");
      if (textarea) {
        textarea.value = sampleText;

        // Update char counter
        if (charCount) {
          charCount.textContent = sampleText.length;
        }

        // Focus so the user can edit if needed
        textarea.focus();
      }
    });
  });


  // ------------------------------------------------------------------
  // 3. FORM VALIDATION — prevent empty or too-short submissions
  // ------------------------------------------------------------------
  const reviewForm = document.getElementById("review-form");

  if (reviewForm) {
    reviewForm.addEventListener("submit", function (e) {
      const text = textarea ? textarea.value.trim() : "";

      if (text.length === 0) {
        e.preventDefault();
        showInlineError("Please enter a review before submitting.");
        textarea.focus();
        return;
      }

      if (text.length < 5) {
        e.preventDefault();
        showInlineError("Review is too short. Please write at least 5 characters.");
        textarea.focus();
        return;
      }

      // Show loading state on the button
      const btn = document.getElementById("submit-btn");
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing…';
      }
    });
  }


  // ------------------------------------------------------------------
  // 4. INLINE ERROR HELPER
  // ------------------------------------------------------------------
  function showInlineError(message) {
    // Remove any existing inline error
    const existing = document.getElementById("inline-error");
    if (existing) existing.remove();

    const div = document.createElement("div");
    div.id = "inline-error";
    div.className = "alert alert-warning d-flex align-items-center gap-2 mt-3";
    div.innerHTML = `<i class="bi bi-exclamation-triangle-fill"></i>${message}`;

    if (reviewForm) {
      reviewForm.appendChild(div);

      // Auto-dismiss after 4 seconds
      setTimeout(() => {
        if (div && div.parentNode) div.remove();
      }, 4000);
    }
  }


  // ------------------------------------------------------------------
  // 5. DASHBOARD — auto-submit filter dropdowns on change (optional UX)
  // ------------------------------------------------------------------
  const filterSelects = document.querySelectorAll(
    "#filter-sentiment, #filter-category, #filter-status"
  );

  filterSelects.forEach(function (select) {
    select.addEventListener("change", function () {
      const form = document.getElementById("filter-form");
      if (form) form.submit();
    });
  });


  // ------------------------------------------------------------------
  // 6. AUTO-DISMISS FLASH MESSAGES after 5 seconds
  // ------------------------------------------------------------------
  const alerts = document.querySelectorAll(".alert.fade.show");

  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

});
