import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function PrivacyPolicy() {
  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6 font-inter">
      <h1 className="text-3xl font-bold text-center">Privacy Policy</h1>
      <p className="text-gray-600 text-center">Effective Date: 2/3/2025</p>
      
      <Card className="pt-2 pb-6 px-6 shadow-md">
        <ScrollArea className="h-[60vh] overflow-y-auto p-4 space-y-6">
          <section>
            <h2 className="text-xl font-semibold pb-2">1. What Data We Collect</h2>
            <p>
              User credentials (ID & password): Used only for login automation, never stored.
              Timetable data: Scraped from your academic portal to generate an iCal file.
              <br />
              Class logs: We may log class schedule without personal identifiers other than the email ID to ensure functionality.
            </p>
          </section>
          
          <section>
            <h2 className="text-xl font-semibold pt-8 pb-2">2. How We Use Your Data</h2>
            <p>
              Credentials are used only during the session and discarded immediately.
              Timetable data is not stored permanently.
              Logged class details help improve service reliability.
            </p>
          </section>
          
          <section>
            <h2 className="text-xl font-semibold pt-8 pb-2">3. Disclaimer</h2>
            <p>
            ClassConnect is an independent tool designed to simplify scheduling and is not affiliated with or endorsed by Academia. <br />
            While we strive for accuracy and reliability, we do not guarantee that the generated schedules will always be free of errors. <br />

            </p>
          </section>
          
          <section>
            <h2 className="text-xl font-semibold pt-8 pb-2">4. Security Measures</h2>
            <p>
              We process all credentials securely and never store them. <br />
              We do not share, sell, or distribute any user data to third parties.
            </p>
          </section>
          
          <section>
            <h2 className="text-xl font-semibold pt-8 pb-2">5. Your Rights</h2>
            <p>
              You can stop using ClassConnect at any time.
              Since we do not store your data, no additional action is required to delete your information.
            </p>
          </section>
          
          <section>
            <h2 className="text-xl font-semibold pt-8 pb-2">6. Changes to Privacy Policy</h2>
            <p>
              We may update this policy from time to time. Continued use of ClassConnect means you accept any updates.
              Please check for updates regularly to stay informed of any changes that may affect your data privacy.
            </p>
          </section>
        </ScrollArea>
      </Card>
    </div>
  );
}
