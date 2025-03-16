import { fetchFromBackend } from "@/lib/api-utils";

export async function GET(request: Request) {
  return fetchFromBackend("sales/sales_summary", request)
}
