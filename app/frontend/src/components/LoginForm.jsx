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
  const [isSubmitting, setIsSubmitting] = useState(false);
  
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

    if (isSubmitting) return;

    setIsSubmitting(true);
    setProgress({ text: "Logging in...", value: 20 });

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
    } finally {
      if (!isLoggedIn) {
        setIsSubmitting(false);
      }
    }
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-3xl pb-1 font-inter font-semibold ">Login</CardTitle>
          <CardDescription className="font-semibold">
            Enter your SRM Academia's Mail ID and Password.
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
                <div className="relative">
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="pass*ord"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="pr-10" 
              />
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="absolute right-0 top-0 h-full px-3 hover:bg-transparent"
                onClick={togglePasswordVisibility}
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                <span className="sr-only">{showPassword ? "Hide password" : "Show password"}</span>
              </Button>
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

      <div className="mt-1 flex items-center justify-center space-x-2">
        <Lock className="h-4 w-4" />
        <p className="font-robotoCondensed text-slate-300 text-base font-medium" >We respect your privacy – no data stored.</p>
      </div>

    </div>
  );
}