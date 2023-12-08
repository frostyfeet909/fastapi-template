export async function fetch_json_with_retry(
    endpoint: string,
    maxRetries: number = 3,
    retryDelay: number = 1000
  ): Promise<any> {
    let retries = 0;
  
    while (retries < maxRetries) {
      try {
        const response = await fetch(endpoint);
  
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log(response.body);
        return await response.json();
      } catch (error) {
        console.error(`Error fetching data from ${endpoint}: ${error.message}`);
        retries++;
  
        if (retries < maxRetries) {
          console.log(`Retrying in ${retryDelay / 1000} seconds...`);
          await new Promise((resolve) => setTimeout(resolve, retryDelay));
        } else {
          console.error(`Max retries (${maxRetries}) reached. Giving up.`);
          throw error; // You can choose to rethrow the error or handle it as needed.
        }
      }
    }
  }