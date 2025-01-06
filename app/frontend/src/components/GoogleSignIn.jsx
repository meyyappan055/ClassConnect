import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;


export function GoogleSignIn() {
  const navigate = useNavigate();

  const handleSuccess = async (credentialResponse) => {
    try {
      console.log('Login Success - Full Response:', credentialResponse);
      navigate('/'); // as of now
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  if (!GOOGLE_CLIENT_ID) {
    console.error('Missing Google Client ID');
    return <div className="text-red-500">Configuration Error: Missing Google Client ID</div>;
  }

  return (
    <div className="flex flex-col items-center">
      <div className="mt-28 mb-10 font-semibold font-inter text-3xl text-center">
        Data scraped successfully from Academia! <br />
        Sign in to effortlessly schedule it into your calendar.
      </div>

      <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
        <GoogleLogin
          onSuccess={handleSuccess}
          onError={(error) => console.error('Login Failed:', error)}
          useOneTap={false}
          flow="implicit"
          auto_select={false}
          type="standard"
          theme="outline"
          size="large"
          text="signin_with"
          shape="rectangular"
          width="200"
          locale="en"
          context="signin"
          ux_mode="popup"
          // hosted_domain="srmist.edu.in"
        />
      </GoogleOAuthProvider>
    </div>
  );
}