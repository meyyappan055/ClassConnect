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
import { useState } from "react";
import axios from "axios";
import DownloadPage from "@/pages/DownloadPage";
import { useNavigate } from "react-router-dom";


export function LoginForm({ className, ...props }) {

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [fileUrl, setFileUrl] = useState(null);
  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log("Starting login attempt...");
      const url = "http://127.0.0.1:8000/api/login";
      const formData = { email, password };

      const response = await axios.post(url, formData, {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true 
      });

      console.log("Server response:", response.data);
      setIsLoggedIn(true); 
      const data = response.data;

      const generateIcalUrl = "http://127.0.0.1:8000/api/generate-ical";

      const postResponse = await axios.post(generateIcalUrl, data, {
        headers: {
          "Content-Type": "application/json",
        },
        responseType: "blob",
      });
      console.log("iCal file generated successfully");

      const blob = new Blob([postResponse.data], { type: "text/calendar" });
      const download_url = URL.createObjectURL(blob);
      setFileUrl(download_url);

      navigate("/download", { state: { fileUrl: download_url } });

      if (response.data.status === "success") {
        console.log("Login successful!");
      }
    } catch (error) {
      console.error("Full error object:", error);
      
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
          <CardTitle className="text-3xl pb-1 font-semibold">Login</CardTitle>
          <CardDescription className="font-semibold">
            Enter your SRM Mail Id and Password
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
                  value = {email}
                  onChange = {(e)=> setEmail(e.target.value) }
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="password">Password </Label>
                  
                </div>
                <Input 
                id="password" 
                type="password" 
                placeholder="pass*ord" 
                value = {password}
                onChange = {(e)=> setPassword(e.target.value) }
                required 
                />
              </div>
              <Button type="submit" variant="outline" className="w-full font-semibold">
                Login
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      
    </div>
  );
}
