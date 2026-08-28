import { readFile, stat } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import { resolve } from "node:path";

const DEFAULT_HOST = "business-document-intelligence.p.rapidapi.com";
const MAX_DOCUMENT_BYTES = 5 * 1024 * 1024;

function rapidApiKey() {
  const key = (process.env.RAPIDAPI_KEY ?? "").trim();
  if (!key) {
    throw new Error(
      "RAPIDAPI_KEY is not set. Set it in your environment before running this example."
    );
  }
  return key;
}

function rapidApiHost() {
  return (process.env.RAPIDAPI_HOST ?? DEFAULT_HOST).trim() || DEFAULT_HOST;
}

async function readDocument(pathValue) {
  const path = resolve(pathValue);
  const info = await stat(path);

  if (!info.isFile()) {
    throw new Error(`Document is not a file: ${path}`);
  }
  if (info.size === 0) {
    throw new Error("Document is empty.");
  }
  if (info.size > MAX_DOCUMENT_BYTES) {
    throw new Error(
      `Document is ${info.size} bytes; the API maximum is ${MAX_DOCUMENT_BYTES} bytes (5 MiB).`
    );
  }

  return { path, body: await readFile(path) };
}

export async function postDocument(endpoint, documentPath) {
  const { path, body } = await readDocument(documentPath);
  const host = rapidApiHost();
  const requestId = `example.${randomUUID()}`;

  const response = await fetch(`https://${host}${endpoint}`, {
    method: "POST",
    headers: {
      "content-type": "application/octet-stream",
      "x-rapidapi-host": host,
      "x-rapidapi-key": rapidApiKey(),
      "x-request-id": requestId,
    },
    body,
  });

  const returnedRequestId = response.headers.get("x-request-id");
  if (returnedRequestId) {
    console.error(`X-Request-ID: ${returnedRequestId}`);
  }

  const text = await response.text();
  let payload;
  try {
    payload = JSON.parse(text);
  } catch {
    payload = { raw_response: text };
  }

  if (!response.ok) {
    throw new Error(
      `API request failed for ${path} with HTTP ${response.status}:\n${JSON.stringify(payload, null, 2)}`
    );
  }

  if (payload === null || Array.isArray(payload) || typeof payload !== "object") {
    throw new Error("API returned a successful response that was not a JSON object.");
  }

  return payload;
}
