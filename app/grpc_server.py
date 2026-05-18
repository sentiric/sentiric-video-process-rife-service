# [ARCH-COMPLIANCE] SOP-01: Eksiksiz Teslimat
import grpc, asyncio, uuid, structlog
from concurrent import futures
from sentiric.video.v1 import gateway_pb2, gateway_pb2_grpc
from app.core.engine import rife_engine
from app.core.config import settings

logger = structlog.get_logger()

class RIFEGatewayServicer(gateway_pb2_grpc.VideoGatewayServiceServicer):
    async def SubmitVideoJob(self, request, context):
        metadata = dict(context.invocation_metadata())
        trace_id = metadata.get("x-trace-id", "unknown")
        tenant_id = metadata.get("x-tenant-id", "unknown")
        job_id = str(uuid.uuid4())

        logger.info(f"RIFE refinement request accepted", event_id="GRPC_JOB_ACCEPTED", trace_id=trace_id)
        
        asyncio.create_task(
            rife_engine.process_video(request.prompt, job_id, trace_id, tenant_id)
        )

        return gateway_pb2.SubmitVideoJobResponse(accepted=True, job_id=job_id)

async def serve_grpc():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=2))
    gateway_pb2_grpc.add_VideoGatewayServiceServicer_to_server(RIFEGatewayServicer(), server)
    listen_addr = f"[::]:{settings.GRPC_PORT}"
    
    try:
        with open(settings.KEY_PATH, "rb") as f: pk = f.read()
        with open(settings.CERT_PATH, "rb") as f: cert = f.read()
        with open(settings.GRPC_TLS_CA_PATH, "rb") as f: ca = f.read()
        
        creds = grpc.ssl_server_credentials([(pk, cert)], root_certificates=ca, require_client_auth=True)
        server.add_secure_port(listen_addr, creds)
        logger.info(f"gRPC mTLS Server Ready on {listen_addr}", event_id="GRPC_SERVER_START")
    except Exception as e:
        logger.error(f"mTLS Fail: {e}", event_id="MTLS_FAIL"); raise e

    await server.start()
    await server.wait_for_termination()