import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value?: number | string;
  icon?: LucideIcon;
  loading?: boolean;
}

export function StatCard({ label, value, icon: Icon, loading }: StatCardProps) {
  return (
    <Card className="border-border/60">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-muted-foreground">{label}</p>
          {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
        </div>
        <div className="mt-3">
          {loading ? (
            <Skeleton className="h-9 w-20" />
          ) : (
            <p className="text-3xl font-semibold tracking-tight tabular-nums">{value ?? "—"}</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
