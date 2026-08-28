import { postDocument } from "./bdi-client.mjs";

const documentPath = process.argv[2];
if (!documentPath) {
  console.error("Usage: node extract-receipt.mjs <receipt.pdf|jpg|png|webp>");
  process.exit(1);
}

try {
  const payload = await postDocument("/v1/receipts/extract", documentPath);
  console.log(JSON.stringify(payload, null, 2));
} catch (error) {
  console.error(`error: ${error instanceof Error ? error.message : String(error)}`);
  process.exit(1);
}
