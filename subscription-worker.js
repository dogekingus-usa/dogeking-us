// Subscription API Worker for Cloudflare Pages
// API key moved to wrangler secret (env.KIT_API_KEY)
// deploy: wrangler deploy --name api-subscribe-worker

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    };
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }
    if (request.method === "POST" && path === "/api/subscribe") {
      let body;
      try {
        body = await request.json();
      } catch (e) {
        return new Response(JSON.stringify({ error: "Invalid JSON" }), {
          status: 400,
          headers: { "Content-Type": "application/json", ...corsHeaders }
        });
      }
      const email = body.email || "";
      const tagId = body.tag_id || "";
      const firstName = body.first_name || "";
      if (!email || !email.includes("@")) {
        return new Response(JSON.stringify({ error: "Valid email is required" }), {
          status: 400,
          headers: { "Content-Type": "application/json", ...corsHeaders }
        });
      }
      try {
        const subscribePayload = { email, first_name: firstName };
        const subscribeRes = await fetch(`${env.KIT_API_BASE || "https://api.kit.com/v4"}/subscribers`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Kit-Api-Key": env.KIT_API_KEY
          },
          body: JSON.stringify(subscribePayload)
        });
        const subscribeData = await subscribeRes.json();
        if (tagId && subscribeData.subscriber?.id) {
          await fetch(`${env.KIT_API_BASE || "https://api.kit.com/v4"}/tags/${tagId}/subscribe`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-Kit-Api-Key": env.KIT_API_KEY
            },
            body: JSON.stringify({ email })
          }).catch(() => {});
        }
        if (!subscribeRes.ok) {
          return new Response(JSON.stringify({ error: "Subscription failed", details: subscribeData }), {
            status: subscribeRes.status,
            headers: { "Content-Type": "application/json", ...corsHeaders }
          });
        }
        return new Response(JSON.stringify({ success: true, message: "Successfully subscribed!", subscriber: subscribeData.subscriber }), {
          status: 200,
          headers: { "Content-Type": "application/json", ...corsHeaders }
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: "Internal error" }), {
          status: 500,
          headers: { "Content-Type": "application/json", ...corsHeaders }
        });
      }
    }
    return new Response(JSON.stringify({ error: "Not found" }), {
      status: 404,
      headers: { "Content-Type": "application/json", ...corsHeaders }
    });
  }
};
