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
import { Spinner } from '@/components/ui/spinner'
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Eye, EyeOff, Lock } from 'lucide-react';  


export function LoginForm({ className, ...props }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState({ text: "", value: 0 });
  const navigate = useNavigate();

  const togglePasswordVisibility = () => setShowPassword(!showPassword);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return;

    setLoading(true);
    setError(null);
    setProgress({ text: "Logging in...", value: 20 });
    

    try {
        const loginResponse = await axios.post("https://classconnect-production.up.railway.app/api/login", 
            { email, password },
            {
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                withCredentials: true
            }
        );

        const task_id = loginResponse.data.task_id;
        console.log("Task started:", task_id);
        setProgress({ text: "Processing your request...", value: 40 });

        const channel = supabase
          .channel(`task-${task_id}`)
          .on('postgres_changes', {
                event: 'UPDATE',
                schema: 'public',
                table: 'tasks',
                filter: `task_id=eq.${task_id}`
            }, async (payload) => {
                console.log("Task update received:", payload.new.status);
                
                if (payload.new.status === 'completed') {
                    setProgress({ text: "Generating calendar...", value: 80 });

                    try {
                        const { data, error } = await supabase
                            .from('tasks')
                            .select('result')
                            .eq('task_id', task_id)
                            .single();
                        
                        if (error) throw error;
                        
                        if (!data || !data.result) {
                          console.error("No result found for task:", task_id);
                          setError("No data available. Please try again.");
                          return;
                      }
                        
                        console.log("Retrieved data from Supabase:", data.result);

                        const postResponse = await axios.post(
                            "https://classconnect-production.up.railway.app/api/generate-ical",
                            { data: data.result },
                            {
                                headers: { 
                                    "Content-Type": "application/json",
                                    "Accept": "application/json"
                                },
                                responseType: "blob"
                            }
                        );
                        
                        console.log("Calendar generation successful");
                        
                        // Mark data as retrieved
                        await supabase
                            .from('tasks')
                            .update({ data_retrieved: true })
                            .eq('task_id', task_id);
                        
                        const blob = new Blob([postResponse.data], { type: "text/calendar" });
                        const download_url = URL.createObjectURL(blob);
                        navigate("/download", { state: { fileUrl: download_url } });

                        await supabase
                            .from('tasks')
                            .delete()
                            .eq('task_id', task_id);

                    } catch (error) {
                        console.error("Generate iCal error:", error);
                        setError("Failed to generate calendar: " + (error.message || "Unknown error"));
                    } finally {
                        channel.unsubscribe();
                        setLoading(false);
                    }
                } else if (payload.new.status === 'failed') {
                    setError(payload.new.error || "Task failed");
                    channel.unsubscribe();
                    setLoading(false);
                }
            });

        const { error: subError } = channel.subscribe();
        if (subError) {
            console.error("Subscription error:", subError);
            setError("Failed to monitor task status");
            setLoading(false);
        }

    } catch (error) {
        console.error("Login error:", error);
        setError(error.response?.data?.detail || "Login failed");
        setLoading(false);
    }
  };


  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-3xl pb-1 font-inter font-semibold">Login</CardTitle>
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
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="password">Password</Label>
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
                    <span className="sr-only">
                      {showPassword ? "Hide password" : "Show password"}
                    </span>
                  </Button>
                </div>
              </div>
              <Button 
                type="submit" 
                variant="outline" 
                className="w-full font-medium text-base"
                disabled={loading}
              >
                {loading ? "Processing..." : "Login"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {progress.text && (
        <div className="w-full space-y-2">
          <Progress value={progress.value} className="w-full mt-1" />
          <div className="flex justify-center items-center gap-2 font-inter font-semibold">
            {loading && <Spinner className="h-7 w-6" />}
            <div className="text-slate-300">{progress.text}</div>
          </div>
        </div>
      )}

      {error && (
        <div className="text-red-500 text-center font-medium">
          Error : {error}
        </div>
      )}

      <div className="mt-1 flex items-center justify-center space-x-2">
        <Lock className="h-5 w-6" />
        <p className="font-robotoCondensed text-slate-300 text-base font-medium">
          We respect your privacy – no data stored.
        </p>
      </div>
    </div>
  );
}