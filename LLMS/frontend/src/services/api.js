/*
----------------------------------------------------
api.js

Purpose
-------
Communicate with the FastAPI backend.

Responsibilities

1. Send prompt to FastAPI
2. Receive generated response
3. Return response to React
----------------------------------------------------
*/

import axios from "axios";

// FastAPI Base URL
const API = axios.create({

    baseURL: "http://127.0.0.1:8000"

});

// Function to call /predict API
export async function generateText(prompt) {

    try {

        const response = await API.post(

            "/predict",

            {
                text: prompt
            }

        );

        return response.data.generated_text;

    }

    catch (error) {

        console.error("API Error:", error);

        throw error;

    }

}