const config = {
    development: {
      API_URL: "http://localhost:8000",
    },
    production: {
      API_URL: "https://basf-app-service-chgsevh6hqebdjad.canadacentral-01.azurewebsites.net",
    },
  };
  
  export default config[process.env.NODE_ENV || "development"];