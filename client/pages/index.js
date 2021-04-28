import Head from 'next/head'
import styles from '../styles/Home.module.css'
import Link from 'next/link'
import { Layout } from '../components'

const searchEndpoint = 'http://localhost:5000/api/v1.0/search'


export default function Home() {
  return (
    <Layout>
    <Head>
      <title>KaibouNews - Home Page</title>
    </Head>
    <h1 className="title">
      Read{' '}
      <Link href="/search-results">
        <a>this page!</a>
      </Link>
    </h1>
    </Layout>
  )
}
