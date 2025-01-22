import axios from "axios";

export function GoogleSignIn() {


  return (
    <div className="flex flex-col items-center">
      <div className="mt-28 mb-10 font-semibold font-inter text-3xl text-center">
        Data scraped successfully from Academia! <br />
        Sign in to effortlessly schedule it into your calendar.
      </div>

      <button
        className="px-6 text-white rounded-xl font-medium border-white border-1 p-2"
      >
        Sign in with Google
      </button>
    </div>
  );
}