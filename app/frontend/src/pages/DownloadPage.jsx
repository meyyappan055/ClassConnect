import React from 'react'
import { useLocation } from "react-router-dom";


const DownloadPage = () => {
    const location = useLocation();
    const fileUrl = location.state?.fileUrl;

    const handleDownload = () => {
          if (fileUrl){
          const link = document.createElement("a");
          link.href = fileUrl;
          link.download = "classes.ics"; 
          link.click();
          }
        }
    
        return (
          <div>
            {fileUrl ? (
              <div className="flex flex-col items-center mt-12">
                <div className="text-3xl pb-1 font-semibold text-center">
                  Your file is ready!
                </div>
                <button
                  onClick={handleDownload}
                  className="mt-4 w-full max-w-xs font-semibold border rounded-lg px-4 py-2 text-center"
                >
                  Download
                </button>
              </div>
            ) : (
              <div className="text-center text-2xl mt-40 text-red-500 font-semibold">No file available to download , Kindly <a className='underline ' href="/login">Login</a> first. </div>
            )}
          </div>
        );
      };
      
export default DownloadPage;