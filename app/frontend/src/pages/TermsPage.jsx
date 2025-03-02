import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";


export default function TermsPage() {
  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6 font-inter">
      <h1 className="text-3xl font-bold text-center">Terms of Service</h1>
      <p className="text-gray-600 text-center">Effective Date: 2/3/2025</p>
      
      <Card className="pt-2 pb-6 px-6 shadow-md">
        <ScrollArea className="h-[60vh] overflow-y-auto p-4 space-y-6 ">
          <section>
            <h2 className="text-xl font-semibold pt-2 pb-2">1. Service Overview</h2>
            <p>
              ClassConnect automates the retrieval of timetable data from your academic portal and converts it into an iCalendar (.ics) file.
              This service is not affiliated with Academia.
            </p>
          </section>
          
          <section>
            <h2 className="text-xl font-semibold pt-8 pb-2">2. User Responsibility</h2>
            <p>
              By using ClassConnect, you confirm that you have the right to access your academic data. ClassConnect is not responsible for any actions taken by your institution
              regarding automated access.
            </p>
          </section>
          
          <section>
            <h2 className="text-xl font-semibold pt-8 pb-2">3. Data Handling</h2>
            <p>
              Credentials are not stored beyond the login session. Timetable data is only processed temporarily to generate an iCal file.
              Class schedule details may be logged temporarily for debugging purposes, but they do not include personal identifiers other than the email ID.
            </p>
          </section>
          
          <section>
            <h2 className="text-xl font-semibold pt-8 pb-2">4. Limitation of Liability</h2>
            <p>
              ClassConnect is provided "as is" with no guarantees. We are not responsible for any issues arising from the use of automation,
              including but not limited to service blocks or changes in Academia’s system.
            </p>
          </section>
          
          <section>
            <h2 className="text-xl font-semibold pt-8 pb-2">5. Updates to ToS</h2>
            <p>
            We may update these terms as needed. Continued use of ClassConnect means you accept any updates. Please check for updates regularly to ensure you are aware of any changes that may affect your use of the service.
            </p>
          </section>
        </ScrollArea>
      </Card>
    </div>
  );
}
