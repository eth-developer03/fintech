import { Box } from '@mui/material';
import Header from '../../components/Header';

const Line = () => {
  return (
    <div className="p-8 bg-gray-900 min-h-screen">
      <Header title="About Us" />
      <div className="text-gray-100 mt-8 space-y-6">
        <h1 className="text-4xl font-bold text-blue-400">Welcome to FINITY</h1>
        <p className="text-lg leading-7">
          At FINITY, we believe in <strong>"Finances Unified"</strong>. Our
          mission is simple yet profound: to provide you with a seamless,
          all-in-one platform that not only manages but also elevates your
          investment journey.
        </p>
        <p className="text-lg leading-7">
          Managing finances can be complex and overwhelming. That's why we've
          designed a platform that simplifies this process, giving you a
          comprehensive view of your investments and offering in-depth insights
          across a diverse range of asset classes, including Stocks, Mutual
          Funds, Bonds, and precious metals like Gold.
        </p>

        <h2 className="text-2xl font-semibold text-blue-300">Our Services</h2>
        <p className="text-lg leading-7">
          Our suite of services is tailored to meet the needs of every investor,
          from novices to seasoned professionals. We pride ourselves on our
          cutting-edge portfolio rebalancing services, our sentiment-based stock
          simulator that helps you gauge the market mood, and our personalized
          chatbot designed to quench your financial curiosities. Our platform is
          not just a tool but a companion on your financial journey.
        </p>

        <h2 className="text-2xl font-semibold text-blue-300">Meet Our Team</h2>
        <p className="text-lg leading-7">
          Behind FINITY's innovative platform is a team of passionate,
          dedicated, and incredibly talented individuals:
        </p>

        <div className="space-y-4">
          <div>
            <strong className="text-blue-300">Karthik Nambiar:</strong>
            <p>
              A wizard in Python Development and Deep Learning, Karthik brings
              over a year of capital market experience to the table. His
              expertise and innovative approach to financial technologies drive
              the core development of our platform, ensuring that FINITY remains
              at the forefront of financial management solutions.
            </p>
          </div>

          <div>
            <strong className="text-blue-300">Kartikeya Pandey:</strong>
            <p>
              The backbone of our platform, Kartikeya's proficiency in backend
              development with Node and frontend magic with React, creates a
              seamless, intuitive, and dynamic user experience. Her innovative
              approach to development ensures that FINITY is not just functional
              but also a joy to use.
            </p>
          </div>

          <div>
            <strong className="text-blue-300">Garv Trivedi:</strong>
            <p>
              A talented web developer with a strong focus on creating
              responsive and intuitive user interfaces. Garv's expertise in
              modern web development frameworks ensures a seamless and engaging
              experience for our users. His dedication to front-end excellence
              plays a pivotal role in making FINITY's platform both accessible
              and enjoyable to navigate.
            </p>
          </div>

          <div>
            <strong className="text-blue-300">Aman Mehra:</strong>
            <p>
              Not just our team's aesthetic charm, Aman's presence brings an
              unparalleled level of charisma and energy to FINITY. His
              devastatingly handsome looks are matched only by his commitment to
              making financial management both engaging and enjoyable for
              everyone.
            </p>
          </div>
        </div>

        <p className="text-lg leading-7">
          Together, we are <strong className="text-blue-400">FINITY</strong> – a
          team united by a shared vision of demystifying finance and making it
          accessible to all. We're not just about numbers and algorithms; we're
          about empowering you to make informed financial decisions with
          confidence and clarity. Join us on this journey, and let's redefine
          the future of finance, together.
        </p>

        <h2 className="text-2xl font-bold text-blue-400">Welcome to FINITY</h2>
      </div>
    </div>
  );
};

export default Line;
