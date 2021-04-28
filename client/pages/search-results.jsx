import Link from 'next/link'
import Head from 'next/head'
import { Layout } from '../components'

export default function SearchResults() {
    return (
        <>
        <Layout>
            <Head>
            <title>KaibouNews - Search Results</title>
            </Head>
            <h2>
            <Link href="/">
                <a>Back to home</a>
            </Link>
            </h2>
        </Layout>
      </>
    )
  }