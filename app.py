import sys
import logging
from flask import Flask, render_template_string, request, session, jsonify
from flask_socketio import SocketIO, emit, disconnect

# --- CONFIGURATION & LOGGING ---
# In a real production env, use environment variables for these
ADMIN_PASSWORD = "admin"
SECRET_KEY = "ux4g_secure_key_production_v1"
PORT = 5000

# Configure logging for production debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# manage_session=False ensures better compatibility with mobile browsers dropping cookies
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# --- FRONTEND APPLICATION (React + Ant Design + UX4G Styles) ---
# We use {% raw %} blocks to prevent Jinja2 from conflicting with React's curly braces.

FRONTEND_TEMPLATE = """
{% raw %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>NetWatch Pro | UX4G Compliant</title>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.5/babel.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/antd/5.12.2/reset.min.css"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.11.10/dayjs.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/antd/5.12.2/antd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://unpkg.com/@ant-design/icons/dist/index.umd.js"></script>

    <style>
        :root {
            --primary-color: #1890ff;
            --success-color: #52c41a;
            --bg-color: #f0f2f5;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 0;
        }
        .header {
            background: #fff;
            padding: 16px 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .brand {
            font-weight: 700;
            font-size: 18px;
            color: #000;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .brand span { color: var(--primary-color); }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 0 16px;
        }
        .video-wrapper {
            position: relative;
            background: #000;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            aspect-ratio: 4/3;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        video, img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .controls-overlay {
            position: absolute;
            bottom: 20px;
            left: 0;
            right: 0;
            display: flex;
            justify-content: center;
            gap: 16px;
            z-index: 10;
        }
        .text-center { text-align: center; }
        .mt-4 { margin-top: 16px; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;
        const { Button, Input, Card, Typography, Spin, message, Modal, Alert, Tag, Space } = window.antd;
        const {
            VideoCameraOutlined,
            EyeOutlined,
            LockOutlined,
            SwapOutlined,
            PoweroffOutlined,
            WifiOutlined,
            DisconnectOutlined
        } = window.icons;
        const { Title, Text } = Typography;

        const socket = io();

        const Login = ({ onLogin }) => {
            const [loading, setLoading] = useState(false);
            const [password, setPassword] = useState("");

            const handleLogin = async () => {
                if (!password) return message.warning("Please enter the password");
                setLoading(true);
                try {
                    const res = await fetch('/api/verify', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ password })
                    });
                    const data = await res.json();
                    if (data.success) {
                        message.success("Access Granted");
                        onLogin();
                    } else {
                        message.error("Access Denied");
                    }
                } catch (e) {
                    message.error("Network Error");
                }
                setLoading(false);
            };

            return (
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                    <Card style={{ width: 350, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
                        <div className="text-center" style={{ marginBottom: 24 }}>
                            <LockOutlined style={{ fontSize: 32, color: '#1890ff' }} />
                            <Title level={3}>Secure Access</Title>
                        </div>
                        <Space direction="vertical" style={{ width: '100%' }}>
                            <Input.Password
                                placeholder="Admin Password"
                                size="large"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                onPressEnter={handleLogin}
                            />
                            <Button type="primary" block size="large" onClick={handleLogin} loading={loading}>
                                Authenticate
                            </Button>
                        </Space>
                    </Card>
                </div>
            );
        };

        const CameraUnit = () => {
            const videoRef = useRef(null);
            const canvasRef = useRef(null);
            const [streaming, setStreaming] = useState(false);
            const [facingMode, setFacingMode] = useState('environment');
            const [socketStatus, setSocketStatus] = useState('disconnected');

            useEffect(() => {
                socket.on('connect', () => setSocketStatus('connected'));
                socket.on('disconnect', () => setSocketStatus('disconnected'));
                return () => socket.off();
            }, []);

            const startCamera = async () => {
                try {
                    if (videoRef.current && videoRef.current.srcObject) {
                        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
                    }
                    const stream = await navigator.mediaDevices.getUserMedia({
                        video: { facingMode: facingMode, width: { ideal: 640 }, height: { ideal: 480 } }
                    });
                    videoRef.current.srcObject = stream;
                    setStreaming(true);
                } catch (err) {
                    Modal.error({ title: 'Camera Error', content: 'Check permissions or use HTTPS/localhost.' });
                }
            };

            useEffect(() => { if (streaming) startCamera(); }, [facingMode]);

            useEffect(() => {
                let interval;
                if (streaming) {
                    interval = setInterval(() => {
                        const ctx = canvasRef.current.getContext('2d');
                        canvasRef.current.width = videoRef.current.videoWidth;
                        canvasRef.current.height = videoRef.current.videoHeight;
                        ctx.drawImage(videoRef.current, 0, 0);
                        socket.emit('frame_upload', canvasRef.current.toDataURL("image/jpeg", 0.4));
                    }, 100);
                }
                return () => clearInterval(interval);
            }, [streaming]);

            return (
                <div className="container">
                    <Alert message={socketStatus === 'connected' ? "Online" : "Offline"} type={socketStatus === 'connected' ? "success" : "error"} showIcon />
                    <div className="video-wrapper mt-4">
                        <video ref={videoRef} autoPlay playsInline muted />
                        <div className="controls-overlay">
                            {!streaming ? (
                                <Button type="primary" size="large" onClick={startCamera}>Start</Button>
                            ) : (
                                <Button size="large" icon={<SwapOutlined />} onClick={() => setFacingMode(f => f==='user'?'environment':'user')} />
                            )}
                        </div>
                    </div>
                    <canvas ref={canvasRef} style={{ display: 'none' }} />
                </div>
            );
        };

        const MonitorUnit = () => {
            const [imageSrc, setImageSrc] = useState(null);
            useEffect(() => {
                socket.on('frame_stream', (data) => setImageSrc(data));
                return () => socket.off('frame_stream');
            }, []);
            return (
                <div className="container">
                    <div className="video-wrapper">
                        {imageSrc ? <img src={imageSrc} /> : <Spin size="large" />}
                    </div>
                </div>
            );
        };

        const App = () => {
            const [route, setRoute] = useState(window.location.pathname);
            const [isAuthenticated, setIsAuthenticated] = useState(false);
            const navigate = (path) => { window.history.pushState({}, '', path); setRoute(path); };

            let content;
            if (route === '/camera') content = <CameraUnit />;
            else if (route === '/screen') content = isAuthenticated ? <MonitorUnit /> : <Login onLogin={() => setIsAuthenticated(true)} />;
            else content = (
                <div className="container text-center" style={{ marginTop: 50 }}>
                    <Space direction="vertical">
                        <Button type="primary" onClick={() => navigate('/camera')}>Camera Mode</Button>
                        <Button onClick={() => navigate('/screen')}>Monitor Mode</Button>
                    </Space>
                </div>
            );

            return (
                <>
                    <header className="header">
                        <div className="brand" onClick={() => navigate('/')}>NetWatch<span>Pro</span></div>
                    </header>
                    {content}
                </>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
{% endraw %}
"""


# --- FLASK ROUTES ---

@app.route('/')
@app.route('/camera')
@app.route('/screen')
def index():
    # React Router (Client-side) handles the actual view based on URL
    return render_template_string(FRONTEND_TEMPLATE)

@app.route('/api/verify', methods=['POST'])
def verify_password():
    data = request.get_json()
    if data.get('password') == ADMIN_PASSWORD:
        session['logged_in'] = True
        return jsonify({"success": True})
    return jsonify({"success": False}), 401

# --- SOCKET EVENTS ---

@socketio.on('frame_upload')
def handle_frame(data):
    # Broadcast to all clients except sender
    emit('frame_stream', data, broadcast=True, include_self=False)

@socketio.on('connect')
def handle_connect():
    logger.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

# --- ENTRY POINT ---

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

@app.after_request
def add_security_headers(response):
    # This header is CRITICAL for tunnels like Cloudflare
    # It explicitly allows the 'camera' feature
    response.headers['Permissions-Policy'] = 'camera=(self), microphone=()'
    # Standard security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response


if __name__ == '__main__':
    import socket
    ip = get_local_ip()

    print("\n" + "="*50)
    print(f" NETWATCH PRO - SYSTEM ONLINE")
    print(f" Localhost: http://127.0.0.1:{PORT}")
    print(f" Network:   http://{ip}:{PORT}")
    print("="*50 + "\n")

    # Run with standard threading for best Termux compatibility
    socketio.run(app, host='0.0.0.0', port=PORT, allow_unsafe_werkzeug=True)
