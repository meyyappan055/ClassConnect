import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { useState, useEffect } from "react";
import axios from "axios";
import DownloadPage from "@/pages/DownloadPage";
import { useNavigate } from "react-router-dom";
import { Eye, EyeOff, Lock } from 'lucide-react';  


export function LoginForm({ className, ...props }) {
  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [fileUrl, setFileUrl] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();
  const [progress, setProgress] = useState({ text: "", value: 0 });
  
  useEffect(() => {
    if (!isLoggedIn) {
      setProgress({ text: "", value: 0 });
    }
  }, [isLoggedIn]);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log("Starting login attempt...");
      const url = "https://classconnect-production.up.railway.app/api/login";
      const formData = { email, password };
      setProgress({ text: "Logging in and scraping...", value: 25 });

      const response = await axios.post(url, formData, {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true 
      });

      setProgress({ text: "Login successful! Generating iCal file...", value: 50 });
      setIsLoggedIn(true);

      const data = response.data;
      if (data){
        setProgress({ text: "Processing calendar data...", value: 75 });
      }
      const generateIcalUrl = "https://classconnect-production.up.railway.app/api/generate-ical";

      const postResponse = await axios.post(generateIcalUrl, data, {
        headers: {
          "Content-Type": "application/json",
        },
        responseType: "blob",
      });

      setProgress({ text: "Calendar file ready!", value: 100 });

      const blob = new Blob([postResponse.data], { type: "text/calendar" });
      const download_url = URL.createObjectURL(blob);
      setFileUrl(download_url);

      setTimeout(() => {
        navigate("/download", { state: { fileUrl: download_url } });
      }, 500);

    } catch (error) {
      console.error("Full error object:", error);
      setProgress({ text: "Error occurred during login", value: 0 });
      
      let errorMessage = "An error occurred during login";
      if (error.response) {
        errorMessage = error.response.data.detail || error.response.data;
        console.error("Server error response:", error.response.data);
      } else if (error.request) {
        errorMessage = "No response received from server";
      }
      
      console.error("Login failed:", errorMessage);
    }
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-3xl pb-1 font-inter font-semibold ">Login</CardTitle>
          <CardDescription className="font-semibold">
            Enter your SRM Mail ID and Password
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="xyz@srmist.edu.in"
                  value={email}
                  onChange={(e)=> setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="password">Password </Label>
                </div>
                <div className="flex flex-row">
                  <Input 
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="pass*ord" 
                    value={password}
                    onChange={(e)=> setPassword(e.target.value)}
                    required 
                  />
                  <button 
                    type="button"
                    className="absolute ml-76 mt-2"
                    onClick={togglePasswordVisibility}
                  >
                    {showPassword ? <EyeOff size={20}/> : <Eye size={20} />}
                  </button>
                </div>
              </div>
              <Button type="submit" variant="outline" className="w-full font-medium text-base">
                Login
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {progress.text && (
        <div className="w-full space-y-2">
          <Progress value={progress.value} className="w-full" />
          <div className="flex justify-center font-inter font-semibold">
            <div className="text-slate-300">
              {progress.text}
            </div>
          </div>
        </div>
      )}

      <div className="font-inter text-base font-medium text-center mt-1 flex ml-12">
        <div>
          <Lock className="mt-0.5" size={18} color="#8b9388"/>
        </div>
        <div className="ml-2 font-robotoCondensed text-slate-300">
          We respect your privacy – no data stored.
        </div>
      </div>
    </div>
  );
}