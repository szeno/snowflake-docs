# Sep 8, 2026: Shadow traffic for gateways (*Preview*)

With this preview release, you can use a shadow traffic gateway to send all production requests to a primary service endpoint while mirroring a percentage of those requests to one or more shadow endpoints. Responses from shadow endpoints aren’t returned to clients.

Use shadow traffic to evaluate challenger services with production request patterns without directing production responses through those services.

For more information, see [Use Gateways to route ingress requests to multiple endpoints](/developer-guide/snowpark-container-services/gateway).
