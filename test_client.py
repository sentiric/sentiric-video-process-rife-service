import grpc, os, uuid, time
from sentiric.video.v1 import gateway_pb2, gateway_pb2_grpc

def run_test():
    # mTLS
    base_cert_dir = "../sentiric-certificates/certs"
    with open(os.path.join(base_cert_dir, "ca.crt"), "rb") as f: ca = f.read()
    with open(os.path.join(base_cert_dir, "video-process-rife-service-chain.crt"), "rb") as f: cert = f.read()
    with open(os.path.join(base_cert_dir, "video-process-rife-service.key"), "rb") as f: key = f.read()
    
    creds = grpc.ssl_channel_credentials(ca, key, cert)
    with grpc.secure_channel("localhost:16151", creds) as channel:
        stub = gateway_pb2_grpc.VideoGatewayServiceStub(channel)
        
        # Wan2.1'den çıkan videonun S3 URI'sini veriyoruz
        video_uri = "s3://sentiric/videos/92808fa2-fab6-4d45-a00f-d30bbd0de5b1.mp4"
        print(f"🎬 RIFE Refinement Başlatılıyor: {video_uri}")
        
        response = stub.SubmitVideoJob(gateway_pb2.SubmitVideoJobRequest(
            tenant_id="test-tenant", trace_id=str(uuid.uuid4()),
            prompt=video_uri, preferred_model="rife-v4"
        ))
        print(f"✅ KABUL EDİLDİ | ID: {response.job_id}")

if __name__ == "__main__": run_test()