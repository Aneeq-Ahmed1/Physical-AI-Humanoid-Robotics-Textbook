import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container text--center">
        <Heading as="h1" className="hero__title">
          Physical AI & Humanoid Robotics
        </Heading>
        <p className="hero__subtitle">
          A Modern Guide to Embodied Intelligence, Machines, and Human-Robot Futures
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg margin-right--md"
            to="/docs/intro">
            Start Reading
          </Link>
          <Link
            className="button button--primary button--lg margin-horiz--md"
            to="/docs/intro">
            Download PDF
          </Link>
          <Link
            className="button button--outline button--lg margin-left--md"
            to="/docs">
            View Chapters
          </Link>
        </div>
      </div>
    </header>
  );
}

function TextbookFeatures() {
  const features = [
    {
      title: 'Physical AI',
      description: 'Understanding the intersection of artificial intelligence and physical embodiment in robotic systems.'
    },
    {
      title: 'Humanoid Design',
      description: 'Exploring the principles behind creating human-like robots with advanced capabilities.'
    },
    {
      title: 'Sensorimotor Systems',
      description: 'Advanced sensory and motor control systems that enable robots to interact with the world.'
    },
    {
      title: 'Cognitive Architecture',
      description: 'Building intelligent systems that can perceive, reason, and act in complex environments.'
    },
    {
      title: 'Ethics & Safety',
      description: 'Critical examination of the societal implications and safety considerations of humanoid robots.'
    },
    {
      title: 'Human-Robot Interaction',
      description: 'Designing intuitive interfaces and interaction paradigms for seamless human-robot collaboration.'
    }
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {features.map((feature, idx) => (
            <div className="col col--4" key={idx}>
              <div className="text--center padding-horiz--md">
                <Heading as="h3">{feature.title}</Heading>
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Physical AI & Humanoid Robotics`}
      description="A Modern Guide to Embodied Intelligence, Machines, and Human-Robot Futures">
      <HomepageHeader />
      <main>
        <TextbookFeatures />
      </main>
    </Layout>
  );
}
