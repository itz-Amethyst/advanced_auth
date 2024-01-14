export function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Function to check if the input is a positive integer
export function isValidInput(input) {
    const parsedInput = parseInt(input, 10);
    return !isNaN(parsedInput) && parsedInput > 0 && Number.isInteger(parsedInput);
  };