import Link from 'next/link';

export default function Header() {
  return (
    <header>
      <nav>
        <Link href="/">
          <a>Home</a>
        </Link>
        {/* Add other navigation links here */}
      </nav>
    </header>
  );
}
