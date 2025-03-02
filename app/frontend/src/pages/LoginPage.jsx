import { LoginForm } from "../components/LoginForm"

export default function LoginPage() {
  return (
    <div>
      <div className="flex items-center justify-center mt-12 p-6 md:p-10">
        <div className="w-full max-w-sm">
          <LoginForm />
        </div>
      </div>
      <div className="font-inter font-semibold text-slate-300 text-sm flex flex-row items-center mt-14 justify-center">
          <div className="m-2">
            <a href="/privacy">Privacy Policy</a>
          </div>
            <span>
              |
            </span>
          <div className="m-2">
            <a href="/terms">Terms of Service</a>
          </div>
      </div>
    </div>
    
  )
}
