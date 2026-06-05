import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { toast } from "sonner";
import { ArrowRight, Layers, Sparkles, TrendingUp, Mail, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { StatCard } from "@/components/StatCard";
import { getStats, subscribeUser } from "@/services/api";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "The AI Dispatch — Daily AI News, Curated" },
      { name: "description", content: "Daily AI news aggregated, ranked, and summarized by AI." },
    ],
  }),
  component: Home,
});

const features = [
  {
    icon: Layers,
    title: "Multi-source Aggregation",
    body: "We continuously pull stories from the most trusted AI publications and research outlets.",
  },
  {
    icon: TrendingUp,
    title: "AI Story Ranking",
    body: "Every article is scored for importance so only what truly matters reaches your inbox.",
  },
  {
    icon: Sparkles,
    title: "AI Summarization",
    body: "Concise, faithful summaries that respect your time — no fluff, no hype.",
  },
  {
    icon: Mail,
    title: "Daily Newsletter",
    body: "A clean, beautifully formatted dispatch delivered each morning. Ready to read in 5 minutes.",
  },
];

function Home() {
  const stats = useQuery({ queryKey: ["stats"], queryFn: getStats });
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubscribe = async (e: FormEvent) => {
    e.preventDefault();
    if (!email.includes("@")) {
      toast.error("Please enter a valid email");
      return;
    }
    setSubmitting(true);
    try {
      await subscribeUser(email);
      toast.success("Subscribed! Check your inbox tomorrow.");
      setEmail("");
    } catch (err) {
      toast.error("Subscription failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main>
      {/* Hero */}
      <section className="border-b border-border/60">
        <div className="mx-auto max-w-6xl px-4 py-24 md:py-32">
          <div className="mx-auto max-w-3xl text-center">
            <div className="inline-flex items-center gap-2 rounded-full border border-border/60 bg-secondary/50 px-3 py-1 text-xs font-medium text-muted-foreground">
              <span className="h-1.5 w-1.5 rounded-full bg-accent" />
              Updated daily with AI-ranked stories
            </div>
            <h1 className="mt-6 text-5xl font-semibold tracking-tight md:text-6xl">
              The AI Dispatch
            </h1>
            <p className="mt-5 text-lg leading-relaxed text-muted-foreground md:text-xl">
              Daily AI news curated, ranked and summarized using AI.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <Button asChild size="lg">
                <Link to="/newsletter">
                  Read Latest Newsletter <ArrowRight className="ml-1 h-4 w-4" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <a href="#subscribe">Subscribe</a>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section>
        <div className="mx-auto max-w-6xl px-4 py-20">
          <div className="max-w-2xl">
            <h2 className="text-3xl font-semibold tracking-tight md:text-4xl">
              An editorial pipeline, fully automated.
            </h2>
            <p className="mt-3 text-muted-foreground">
              From thousands of headlines to one perfect morning read.
            </p>
          </div>
          <div className="mt-10 grid gap-4 md:grid-cols-2">
            {features.map((f) => (
              <Card key={f.title} className="border-border/60">
                <CardContent className="p-6">
                  <div className="grid h-10 w-10 place-items-center rounded-lg bg-secondary">
                    <f.icon className="h-5 w-5" />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold tracking-tight">{f.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{f.body}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Subscribe */}
      <section id="subscribe" className="border-t border-border/60 bg-secondary/30">
        <div className="mx-auto max-w-3xl px-4 py-20 text-center">
          <h2 className="text-3xl font-semibold tracking-tight md:text-4xl">
            Get the next dispatch
          </h2>
          <p className="mt-3 text-muted-foreground">
            One email each morning. The AI news that matters, summarized for builders and operators.
          </p>
          <form onSubmit={handleSubscribe} className="mx-auto mt-8 flex max-w-md flex-col gap-2 sm:flex-row">
            <Input
              type="email"
              required
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="h-11"
            />
            <Button type="submit" disabled={submitting} size="lg">
              {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : "Subscribe"}
            </Button>
          </form>
          <p className="mt-3 text-xs text-muted-foreground">Free forever. Unsubscribe anytime.</p>
        </div>
      </section>

      <footer className="border-t border-border/60 py-10 text-center text-sm text-muted-foreground">
        © {new Date().getFullYear()} The AI Dispatch
      </footer>
    </main>
  );
}
