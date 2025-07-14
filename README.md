
# Samvaada - A Personal Database Assistant

Samvaada is primarily an Agentic AI Application built using LangGraph to Communicate with Enterprise Database (MySQL) in Natural Language and retrieve data back in a similar Fashion



## LangGraph Architecture

LangGraph Components Can be found in `app/agent`

![Project Screenshot](app/agent/agent_graph_mermaid.png)

Pipeline
| **Node**             | **Description**                                                                  |
| -------------------- | -------------------------------------------------------------------------------- |
| `setup`              | Initializes agent state with schema context, current time, and user input.       |
| `qa`                 | Determines if the user question can be answered without querying the database.   |
| `clarify_query_node` | Reformulates the user question into a clear, standalone, and unambiguous query.  |
| `sql_node`           | Generates and executes the SQL query using the clarified question and context.   |
| `tools`              | Executes the appropriate tool (SQL runner and result saver) via LangChain tools. |
| `response`           | Converts the SQL query result into a natural language answer for the user.       |



## Run Locally

Clone the project

```bash
  git clone https://github.com/FreakQnZ/Samvaada
```

Run Backend

```bash
  cd app
  pip install -r requirements.txt
  uvicorn main:app
```
Run Frontend

```bash
  cd ..
  cd client
  npm install
  npm run dev
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in your app folder (backend)

`MYSQL_USERNAME=username`

`MYSQL_PASSWORD=password`

`GROQ_API_KEY=gorq api key`      Groq API key can be obtained here - https://console.groq.com/keys







## Guidelines

While the Pipeline and overall architecture can be treated as a blackbox, the prompts are enigneered specifically for a specific enterprise database

Prompts may need to be changed to fit your use case

It is also recommended to create a new user in the database which has only read permissions and add these crednetials in the `.env` file

## Feedback

If you have any feedback, please reach out to me at anuraag.srivatsa123@gmail.com

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://anuraagsrivatsa.vercel.app/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anuraag-srivatsa/)
