// Mobile Menu Toggle
document.addEventListener("DOMContentLoaded", () => {
    const mobileMenuBtn = document.getElementById("mobileMenuBtn")
    const mobileNav = document.getElementById("mobileNav")
  
    if (mobileMenuBtn && mobileNav) {
      mobileMenuBtn.addEventListener("click", () => {
        mobileNav.classList.toggle("active")
  
        // Toggle icon between bars and X
        const icon = mobileMenuBtn.querySelector("i")
        if (icon.classList.contains("fa-bars")) {
          icon.classList.remove("fa-bars")
          icon.classList.add("fa-times")
        } else {
          icon.classList.remove("fa-times")
          icon.classList.add("fa-bars")
        }
      })
    }
  
    // Animation on scroll
    const animatedElements = document.querySelectorAll("[data-animate]")
  
    if (animatedElements.length > 0) {
      // Function to check if element is in viewport
      function isInViewport(element) {
        const rect = element.getBoundingClientRect()
        return rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.9 && rect.bottom >= 0
      }
  
      // Function to handle scroll animation
      function handleScrollAnimation() {
        animatedElements.forEach((element) => {
          if (isInViewport(element)) {
            element.classList.add("animate-in")
          }
        })
      }
  
      // Initial check on load
      handleScrollAnimation()
  
      // Check on scroll
      window.addEventListener("scroll", handleScrollAnimation)
    }
  
    // Set current year in footer
    const currentYearElement = document.getElementById("currentYear")
    if (currentYearElement) {
      currentYearElement.textContent = new Date().getFullYear()
    }
  
    // Tab functionality
    const tabButtons = document.querySelectorAll(".tab-button")
    const tabContents = document.querySelectorAll(".tab-content")
  
    if (tabButtons.length > 0 && tabContents.length > 0) {
      tabButtons.forEach((button) => {
        button.addEventListener("click", () => {
          const tabId = button.getAttribute("data-tab")
  
          // Remove active class from all buttons and contents
          tabButtons.forEach((btn) => btn.classList.remove("active"))
          tabContents.forEach((content) => content.classList.remove("active"))
  
          // Add active class to clicked button and corresponding content
          button.classList.add("active")
          document.getElementById(tabId).classList.add("active")
        })
      })
    }
  
    // Visit toggle functionality
    const visitToggles = document.querySelectorAll(".visit-toggle")
  
    if (visitToggles.length > 0) {
      visitToggles.forEach((toggle) => {
        toggle.addEventListener("click", () => {
          const visitCard = toggle.closest(".visit-card")
          const visitDetails = visitCard.querySelector(".visit-details")
          const icon = toggle.querySelector("i")
  
          if (visitDetails.style.display === "none") {
            visitDetails.style.display = "block"
            icon.classList.remove("fa-chevron-down")
            icon.classList.add("fa-chevron-up")
          } else {
            visitDetails.style.display = "none"
            icon.classList.remove("fa-chevron-up")
            icon.classList.add("fa-chevron-down")
          }
        })
      })
    }
  })
  
  