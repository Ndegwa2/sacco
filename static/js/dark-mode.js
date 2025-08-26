// Dark Mode Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
  // Create the toggle button
  const toggleButton = document.createElement('button');
  toggleButton.id = 'darkModeToggle';
  toggleButton.className = 'dark-mode-toggle';
  toggleButton.innerHTML = '🌙';
  toggleButton.setAttribute('aria-label', 'Toggle dark mode');
  
  // Add the button to the body
  document.body.appendChild(toggleButton);
  
  // Check for saved user preference, if any
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
    toggleButton.innerHTML = '☀️';
  }
  
  // Toggle dark mode when button is clicked
  toggleButton.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    
    // Update button icon
    if (document.body.classList.contains('dark-mode')) {
      toggleButton.innerHTML = '☀️';
      localStorage.setItem('theme', 'dark');
    } else {
      toggleButton.innerHTML = '🌙';
      localStorage.setItem('theme', 'light');
    }
  });
});